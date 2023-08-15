import enum

"""该文件主要保存一些enum类"""


# 一些基础的状态类，状态类由enum.Enum作为基类实现
class CharaterAliveEnum(enum.Enum):
    alive = 2
    faint = 1
    dead = 0


class CardTypeEnum(enum.Enum):
    # 基础牌堆
    magic_attack = 1
    physical_attack = 2
    mental_attack = 3
    steal = 4
    armor = 5
    weapon = 6
    status = 7
    healing = 8
    event_trigger = 9
    element = 10
    anti_element = 11


class SpeciesEnum(enum.Enum):
    # 种族
    earth_pony = 1
    unicorn = 2
    pegasi = 3
    alicon = 4

class SpecialNumberEnum(enum.Enum):
    #特殊数字，无限大和强制0
    infinity = 1
    forced_zero = 0