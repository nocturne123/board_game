"""技能模块，所有技能都需要register功能和unregister功能，主动技能需要额外提供use功能"""
from player import Player
from card import Card


class Skill:
    def __init__(self):
        pass


class CharacterSkill(Skill):
    """角色技能"""

    pass


class EquipmentSkill(Skill):
    """装备技能"""

    pass


class SpeciesSkill(Skill):
    """种族技能"""

    pass
