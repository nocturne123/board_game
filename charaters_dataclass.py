from ENUMS import SpeciesEnum
from dataclasses import dataclass


@dataclass
class Charater:
    health: int
    magic_attack: int
    physical_attack: int
    mental_attack: int
    speed: int
    collect_items: tuple = tuple()
    name: str
    species: SpeciesEnum
