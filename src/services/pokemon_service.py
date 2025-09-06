import httpx
from typing import Union, List

from src.models.pokemon_models import (
    Pokemon,
    PokemonType,
    PokemonApiResponse,
    TypeInfo,
    PokemonSprites,
)


class PokemonNotFound(Exception):
    def __init__(self, pokemon_name_or_id: Union[str, int]):
        super().__init__(f"Pokemon not found: {pokemon_name_or_id}")
        self.pokemon_name_or_id = pokemon_name_or_id


class PokemonService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.base_url = "https://pokeapi.co/api/v2"

    async def get_pokemon_info(self, pokemon_name_or_id: Union[str, int]) -> Pokemon:
        try:
            path_segment = str(pokemon_name_or_id).lower()
            response = await self.client.get(f"{self.base_url}/pokemon/{path_segment}")
            response.raise_for_status()  # Raises an HTTPStatusError for 4xx/5xx responses

            pokemon_raw_data = response.json()
            pokemon_api_response = PokemonApiResponse(
                id=pokemon_raw_data["id"],
                name=pokemon_raw_data["name"],
                types=[
                    PokemonType(
                        slot=t_data["slot"],
                        type=TypeInfo(
                            name=t_data["type"]["name"], url=t_data["type"]["url"]
                        ),
                    )
                    for t_data in pokemon_raw_data["types"]
                ],
                sprites=PokemonSprites(
                    front_default=pokemon_raw_data["sprites"]["front_default"]
                ),
            )

            formatted_pokemon_types: List[str] = [
                pokemon_type.type.name for pokemon_type in pokemon_api_response.types
            ]

            return Pokemon(
                id=pokemon_api_response.id,
                name=pokemon_api_response.name,
                types=formatted_pokemon_types,
                imageURL=pokemon_api_response.sprites.front_default,
            )

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PokemonNotFound(pokemon_name_or_id) from e
            raise Exception(
                f"HTTP error retrieving pokemon details for: {pokemon_name_or_id} - {e}"
            ) from e
        except Exception as e:
            raise Exception(
                f"Error retrieving pokemon details for: {pokemon_name_or_id} - {e}"
            ) from e
