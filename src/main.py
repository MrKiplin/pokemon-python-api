from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status
import httpx

from src.services.pokemon_service import PokemonService, PokemonNotFound
from src.models.pokemon_models import Pokemon

app = FastAPI()


async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client


def get_pokemon_service(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> PokemonService:
    return PokemonService(client)


@app.get("/pokemon/{pokemon_name_or_id}", response_model=Pokemon)
async def read_pokemon(
    pokemon_name_or_id: Union[str, int],
    service: PokemonService = Depends(get_pokemon_service),
):
    try:
        pokemon_info = await service.get_pokemon_info(pokemon_name_or_id)
        return pokemon_info
    except PokemonNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )
