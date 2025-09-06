from dataclasses import dataclass
from typing import List


@dataclass
class Pokemon:
    id: int
    name: str
    types: List[str]
    imageURL: str


@dataclass
class TypeInfo:
    name: str
    url: str


@dataclass
class PokemonType:
    slot: int
    type: TypeInfo


@dataclass
class PokemonSprites:
    front_default: str


@dataclass
class PokemonApiResponse:
    id: int
    name: str
    types: List[PokemonType]
    sprites: PokemonSprites
