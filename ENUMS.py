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
    event_trigger = 8
    element = 9


class SpeciesEnum(enum.Enum):
    # 种族
    earth_pony = 1
    unicorn = 2
    pegasi = 3
    alicon = 4
