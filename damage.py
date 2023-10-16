from ENUMS.common_enums import DamageTypeEnum
from dataclasses import dataclass


@dataclass
class Damage:
    num: int
    type: DamageTypeEnum
