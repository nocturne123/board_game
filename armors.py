"""装备，"""
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
        """注册时的效果，也就是生效，卡牌在装备时调用这个函数，进行'生效'。"""
        pass

    @abstractmethod
    def unregister(self, user):
        """注销时的效果，当装备失效时，装备不会从装备栏中消失，而是调用这个函数，进行'失效'。"""
        pass

    def equiped(self, user):
        """装备时的效果"""
        self.register(user)

    def unequiped(self, user):
        """卸下时的效果"""
        self.unregister(user)

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

    def register(self, user):
        user.data.physical_defense += 1
        user.data.magic_defense += 1

    def unregister(self, user):
        user.data.physical_defense -= 1
        user.data.magic_defense -= 1


class Hat(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.hat
        self.description = "Physical Defense +2"

    def register(self, user):
        user.data.physical_defense += 2

    def unregister(self, user):
        user.data.physical_defense -= 2


class Amulet(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.amulet
        self.description = "Magic Defense +2"

    def register(self, user):
        user.data.magic_defense += 2

    def unregister(self, user):
        user.data.magic_defense -= 2


class Glasses(BaseArmor):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = ArmorIdentity.glasses
        self.description = "Mental Defense +2"

    def register(self, user):
        user.data.mental_defense += 2

    def unregister(self, user):
        user.data.mental_defense -= 2
