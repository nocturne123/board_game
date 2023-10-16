"""所有角色的技能枚举，用于索引角色技能"""
import enum


class SkillEnum(enum.Enum):
    """技能枚举"""

    """M6角色的技能"""
    Rarity_1 = 1  # 瑞瑞的1技能，TODO：瑞瑞技能过于弱了，未来可能需要加强

    RainbowDash_1 = 2  # 云宝的1技能
    RainbowDash_2 = 3  # 云宝的2技能

    Applejack_1 = 4  # 苹果杰克的1技能

    Fluttershy_1 = 5  # 柔柔的1技能
    Fluttershy_2 = 6  # 柔柔的2技能

    PinkiePie_1 = 7  # 萍琪的1技能
    PinkiePie_2 = 8  # 萍琪的2技能，TODO：萍琪的2技能需要加强，切换为每打出6张牌，投一个色子，抽取对应数量的牌

    TwilightSparkle_1 = 9  # 紫悦的1技能
    TwilightSparkle_2 = 10  # 紫悦的2技能

    """独角兽的技能"""
    Trixie_1 = 11  # 崔克西的1技能
    Trixie_2 = 12  # 崔克西的2技能

    Sunburst_1 = 13  # 日光的1技能
