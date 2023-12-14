"""装备"""
from card import Card, transtions
from ENUMS.common_enums import CardTypeEnum, CardStateEnum
from ENUMS.armor_card_enums import ArmorIdentity
from abc import abstractmethod
from skill import EquipmentSkill


class BaseArmor(Card):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(
            card_type=CardTypeEnum.armor, states=states, transitions=transitions
        )
        # skill列表里面装装备内部定义的类，在equip的时候实例化
        self.skill = []
        # skill实例化之后装进skill_instance里面，
        # 方便装备卸下时从player_data里面删除
        self.skill_instance = []

    # 装备的技能在装备时实例化，而不是游戏开始卡牌实例化的时候就实例化
    def equiped(self, user):
        """装备时的效果"""
        for skill in self.skill:
            self.skill_instance.append(skill(user))

    # 同理，装备被卸下时应该主动回收技能的实例
    def unequiped(self, user):
        """卸下时的效果"""
        for skill_instance in self.skill_instance:
            skill_instance.unregister()
            if skill_instance in user.data.equipment_skills:
                user.data.equipment_skills.remove(skill_instance)
            self.skill_instance.remove(skill_instance)

    @abstractmethod
    def effect(self, user, target):
        """卡牌产生效果"""
        self.equiped(user)

    def __repr__(self):
        return f"{self.identity}: {self.description}"


class Clothes(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.clothes
        self.description = "Physical Defense +1, Magic Defense +1"
        self.skill.append(Clothes.ClothesSkill)

    class ClothesSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "Clothes"
            self.description = "Physical Defense +1, Magic Defense +1"

        def register(self):
            self.player.data.physical_defense += 1
            self.player.data.magic_defense += 1

        def unregister(self):
            self.player.data.physical_defense -= 1
            self.player.data.magic_defense -= 1


class Hat(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.hat
        self.description = "Physical Defense +2"
        self.skill.append(Hat.HatSkill)

    class HatSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "Hat"
            self.description = "Physical Defense +2"

        def register(self):
            self.player.data.physical_defense += 2

        def unregister(self):
            self.player.data.physical_defense -= 2


class Amulet(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.amulet
        self.description = "Magic Defense +2"
        self.skill.append(Amulet.AmuletSkill)

    class AmuletSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "Amulet"
            self.description = "Magic Defense +2"

        def register(self):
            self.player.data.magic_defense += 2

        def unregister(self):
            self.player.data.magic_defense -= 2


class Glasses(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.glasses
        self.description = "Mental Defense +2"
        self.skill.append(Glasses.GlassesSkill)

    class GlassesSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "Glasses"
            self.description = "Mental Defense +2"

        def register(self):
            self.player.data.mental_defense += 2

        def unregister(self):
            self.player.data.mental_defense -= 2


class Bowknot(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.bowknot
        self.description = "Choose a target, target can't use effect card"
