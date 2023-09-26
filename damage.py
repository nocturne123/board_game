from ENUMS import DamageTypeEnum
from dataclasses import dataclass


@dataclass
class Damage:
    num: int
    type: DamageTypeEnum
