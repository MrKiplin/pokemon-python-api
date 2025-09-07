import pytest
import httpx
from unittest.mock import AsyncMock

from src.pokemon_python_api.services.pokemon_service import (
    PokemonService,
    PokemonNotFound,
)

from src.pokemon_python_api.models.pokemon_models import Pokemon

MOCK_POKEMON_API_RESPONSE_CHARMANDER = {
    "id": 4,
    "name": "charmander",
    "sprites": {
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"
    },
    "types": [
        {
            "slot": 1,
            "type": {"name": "fire", "url": "https://pokeapi.co/api/v2/type/10/"},
        }
    ],
}

MOCK_POKEMON_API_RESPONSE_PIKACHU = {
    "id": 25,
    "name": "pikachu",
    "sprites": {
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
    },
    "types": [
        {
            "slot": 1,
            "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"},
        }
    ],
}


# Using pytest-httpx to mock the httpx.AsyncClient
@pytest.fixture
def mock_httpx_client(httpx_mock):
    """
    A fixture that provides a mocked httpx.AsyncClient.
    Uses httpx_mock from pytest-httpx to intercept requests.
    """
    return httpx.AsyncClient()


@pytest.fixture
def pokemon_service(mock_httpx_client):
    """
    Provides an instance of PokemonService initialized with the mocked client.
    """
    return PokemonService(client=mock_httpx_client)


@pytest.mark.asyncio
async def test_get_pokemon_info_success_by_name(pokemon_service, httpx_mock):
    """
    Test successful retrieval of Pokémon information by name.
    """
    httpx_mock.add_response(
        url="https://pokeapi.co/api/v2/pokemon/charmander",
        json=MOCK_POKEMON_API_RESPONSE_CHARMANDER,
        status_code=200,
    )

    pokemon_info = await pokemon_service.get_pokemon_info("charmander")

    assert isinstance(pokemon_info, Pokemon)
    assert pokemon_info == Pokemon(
        id=4,
        name="charmander",
        types=["fire"],
        imageURL="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
    )


@pytest.mark.asyncio
async def test_get_pokemon_info_success_by_id(pokemon_service, httpx_mock):
    """
    Test successful retrieval of Pokémon information by ID.
    """
    httpx_mock.add_response(
        url="https://pokeapi.co/api/v2/pokemon/25",  # Note: it will call /pokemon/25
        json=MOCK_POKEMON_API_RESPONSE_PIKACHU,
        status_code=200,
    )

    pokemon_info = await pokemon_service.get_pokemon_info(25)

    assert isinstance(pokemon_info, Pokemon)
    assert pokemon_info == Pokemon(
        id=25,
        name="pikachu",
        types=["electric"],
        imageURL="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    )


@pytest.mark.asyncio
async def test_get_pokemon_info_not_found(pokemon_service, httpx_mock):
    """
    Test case where Pokémon is not found (404 response).
    """
    httpx_mock.add_response(
        url="https://pokeapi.co/api/v2/pokemon/nonexistent", status_code=404
    )

    with pytest.raises(PokemonNotFound) as excinfo:
        await pokemon_service.get_pokemon_info("nonexistent")

    assert excinfo.value.pokemon_name_or_id == "nonexistent"
    assert "Pokemon not found: nonexistent" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_pokemon_info_http_error(pokemon_service, httpx_mock):
    """
    Test case for other HTTP errors (e.g., 500 Internal Server Error).
    """
    httpx_mock.add_response(
        url="https://pokeapi.co/api/v2/pokemon/errorpokemon",
        status_code=500,
        content="Internal Server Error",
    )

    with pytest.raises(Exception) as excinfo:
        await pokemon_service.get_pokemon_info("errorpokemon")

    assert "HTTP error retrieving pokemon details" in str(excinfo.value)
    assert "Server error '500 Internal Server Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_pokemon_info_malformed_response(pokemon_service, httpx_mock):
    """
    Test case where the API returns malformed JSON or missing keys.
    This should raise a generic Exception due to Pydantic validation or KeyError.
    """
    malformed_data = {
        "id": 999,
        "name": "malformed",
        # Missing 'types' and 'sprites' keys which are expected
    }
    httpx_mock.add_response(
        url="https://pokeapi.co/api/v2/pokemon/malformed",
        json=malformed_data,
        status_code=200,
    )

    with pytest.raises(Exception) as excinfo:
        await pokemon_service.get_pokemon_info("malformed")

    assert "Error retrieving pokemon details for: malformed - 'types'" in str(
        excinfo.value
    )


@pytest.mark.asyncio
async def test_pokemon_service_initialization():
    """
    Test that PokemonService initializes correctly with a client.
    """
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    service = PokemonService(client=mock_client)
    assert service.client is mock_client
    assert service.base_url == "https://pokeapi.co/api/v2"
