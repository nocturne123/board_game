import enum

"""该文件主要保存一些enum类"""


class CharaterAliveEnum(enum.Enum):
    """一些基础的状态类，用于表示一些基础的状态，如存活，昏迷，死亡等"""

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
    """种族"""

    earth_pony = 1
    unicorn = 2
    pegasi = 3
    alicon = 4


class SpecialNumberEnum(enum.Enum):
    """特殊数字，无限大和强制0"""

    infinity = 1
    forced_zero = 0


class GameModeEnum(enum.Enum):
    """对战模式，用于游戏启动时的分队"""

    FFA = 0
    two_vs_two = 1
    three_vs_three = 2
    FFA_two = 3


class BlockTypeEnum(enum.Enum):
    """地图块类型"""

    grass = 1
    dense_forest = 2
    mountain = 3
    water = 4
    snow = 5

    # 特殊地点

    # 水晶帝国
    crystal_empire = 6
    # 云中城
    cloudsdale = 7
    # 平等镇
    our_town = 8
    # 中心城
    canterlot = 9
    # 暮光城堡
    castle_of_friendship = 10
    # 马哈顿
    manehattan = 11
    # 甜苹果园
    sweet_apple_acres = 12
    # 云宝家
    rainbow_dash_house = 13
    # 市镇厅
    town_hall = 14
    # 巴尔的马
    baltimare = 15
    # 方糖屋
    sugar_cube_corner = 16
    # 柔柔家
    fluttershy_house = 17
    # 珍奇时装店
    carousel_boutique = 18
    # 泽科拉小屋
    zecora_house = 19
    # 旧城堡
    old_castle = 20
    # 谐律之树
    tree_of_harmony = 21
