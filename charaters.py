from ENUMS import SpeciesEnum
from dataclasses import dataclass


@dataclass
class Charater:
    health: int
    magic_attack: int
    physical_attack: int
    mental_attack: int
    speed: int
    name: str
    collect_items: tuple = tuple()
    species: SpeciesEnum
