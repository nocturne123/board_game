from ENUMS import DamageTypeEnum
from dataclasses import dataclass
from player_state_machine import Player


@dataclass
class Damage:
    num: int
    type: DamageTypeEnum
    source: Player
