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

import enum


class CharaterAliveEnum(enum.Enum):
    """一些基础的状态类，用于表示一些基础的状态，如存活，昏迷，死亡等"""

    alive = 2
    fainted = 1
    dead = 0


class CardTypeEnum(enum.Enum):
    # 基础抽牌牌堆
    attack = 1
    steal = 2

    armor = 3
    weapon = 4
    effect = 5
    healing = 6

    event_trigger = 7
    element = 8
    anti_element = 9


class AttackCardTypeEnum(enum.Enum):
    physical = 1
    magic = 2
    mental = 3


class SpeciesEnum(enum.Enum):
    """种族"""

    earth_pony = 1
    unicorn = 2
    pegasi = 3
    alicon = 4
    others = 5


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
    on_taking_effect = 4  # 产生效果时刻
    on_equipment = 5  # 被装备时刻
    get_stolen = 6  # 被偷窃时刻
    on_discard = 7  # 被弃置时刻
    in_discard_pile = 8  # 在弃牌堆里


class CardTargetEnum(enum.Enum):
    """卡牌的目标，包括自己，队友，敌人，所有人"""

    self = 0
    teammate = 1

    singel_enemy = 2
    all_enemy = 3

    all = 4


class DamageTypeEnum(enum.Enum):
    """伤害的类型，包括物理，魔法，精神，真实，治疗"""

    physical = 1
    magic = 2
    mental = 3
    real = 4
