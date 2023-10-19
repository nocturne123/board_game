"""这个文件是治疗类卡牌的具体实现"""
from card import Card, transtions
from ENUMS.common_enums import CardTypeEnum, CardStateEnum
from ENUMS.heal_card_enums import HealingIdentity
from abc import abstractmethod
from player import Player
import math


class HealCard(Card):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(
            card_type=CardTypeEnum.healing, states=states, transitions=transitions
        )

    @abstractmethod
    def effect(self, user, target):
        pass


class Apple(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.apple
        self.description = "Heal 2 HP"

    def effect(self, user: Player, target):
        user.heal(2)

    def __repr__(self):
        return f"Apple: {self.description}"


class Cupcake(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.cupcake
        self.description = "Heal 4 HP"

    def effect(self, user: Player, target):
        user.heal(4)

    def __repr__(self):
        return f"Cupcake: {self.description}"


class Cake(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.cake
        self.description = "Heal half of your lost HP(round down)"

    def effect(self, user: Player, target):
        lost_hp = user.data.max_health - user.data.health
        user.heal(math.floor(lost_hp / 2))

    def __repr__(self):
        return f"Cupcake: {self.description}"
