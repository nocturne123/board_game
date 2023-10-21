"""武器"""
from card import Card, transtions
from ENUMS.common_enums import CardTypeEnum, CardStateEnum
from ENUMS.armor_card_enums import ArmorIdentity
from abc import abstractmethod


class BaseArmor(Card):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(
            card_type=CardTypeEnum.armor, states=states, transitions=transitions
        )

    @abstractmethod
    def register(self, user):
        """注册时的效果"""
        pass

    @abstractmethod
    def unregister(self, user):
        """注销时的效果"""
        pass

    def equip(self, user):
        """装备时的效果"""
        self.register(user)

    def unequip(self, user):
        """卸下时的效果"""
        self.unregister(user)

    @abstractmethod
    def effect(self, user, target):
        """卡牌产生效果"""
        self.equip(user)

    def __repr__(self):
        return f"{self.identity}: {self.description}"


class Clothes(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.clothes
        self.description = "Armor +1"

    def effect(self, user, target):
        user.data.armor += 1
