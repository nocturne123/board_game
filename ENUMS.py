import enum

"""该文件主要保存一些enum类
现阶段的ENUM类有：
    CharaterAliveEnum: 用于表示角色的存活状态
    CardTypeEnum: 用于表示卡牌的类型
    SpeciesEnum: 用于表示角色的种族
    SpecialNumberEnum: 用于表示一些特殊的数字，如无限大和强制0
    GameModeEnum: 用于表示游戏的模式，如FFA，2v2，3v3等
    BlockTypeEnum: 用于表示地图块的类型
    PlayerStateEnum: 用于表示玩家的状态类型
    CardStateEnum: 用于表示卡牌的状态机
    DamageTypeEnum: 用于表示伤害的类型


"""


class CharaterAliveEnum(enum.Enum):
    """一些基础的状态类，用于表示一些基础的状态，如存活，昏迷，死亡等"""

    alive = 2
    fainted = 1
    dead = 0


class CardTypeEnum(enum.Enum):
    # 基础抽牌牌堆
    magic_attack = 1
    physical_attack = 2
    mental_attack = 3
    steal = 4

    armor = 5
    weapon = 6
    effect = 7
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

    crystal_empire = 6  # 水晶帝国
    cloudsdale = 7  # 云中城
    our_town = 8  # 平等镇
    canterlot = 9  # 中心城
    castle_of_friendship = 10  # 暮光城堡
    manehattan = 11  # 马哈顿
    sweet_apple_acres = 12  # 甜苹果园
    rainbow_dash_house = 13  # 云宝家
    town_hall = 14  # 市镇厅
    baltimare = 15  # 巴尔的马
    sugar_cube_corner = 16  # 方糖屋
    fluttershy_house = 17  # 柔柔家
    carousel_boutique = 18  # 珍奇时装店
    zecora_house = 19  # 泽科拉小屋
    old_castle = 20  # 旧城堡
    tree_of_harmony = 21  # 谐律之树


class PlayerStateEnum(enum.Enum):
    """玩家的阶段状态，包括准备阶段，抽牌阶段，出牌阶段，弃牌阶段，结束阶段，等待阶段"""

    wait = 0

    prepare = 1
    draw = 2
    play = 3
    discard = 4
    end = 5


class CardStateEnum(enum.Enum):
    """卡牌的状态，包括在牌堆里，抽牌时，手牌里，打出时，产生效果，弃牌堆里"""

    in_draw_pile = 0
    on_draw = 1  # 被抽取时刻
    in_hand = 2  # 在手牌里
    on_use = 3  # 被打出时刻
    on_choose_target = 4  # 选择目标时刻
    on_taking_effect = 5  # 产生效果时刻
    on_equipment = 6  # 被装备时刻
    get_stolen = 7  # 被偷窃时刻
    on_discard = 8  # 被弃置时刻
    in_discard_pile = 9  # 在弃牌堆里


class DamageTypeEnum(enum.Enum):
    """伤害的类型，包括物理，魔法，精神，真实，治疗"""

    physical = 1
    magic = 2
    mental = 3
    real = 4
    healing = 5
