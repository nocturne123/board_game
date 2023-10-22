"""这个文件是治疗类卡牌的具体实现。
potion和toy有待实现，potion需要写好buff类，toy需要写好玩家的伤害记录逻辑"""
from card import Card, transtions
from ENUMS.common_enums import CardTypeEnum, CardStateEnum
from ENUMS.heal_card_enums import HealingIdentity
from abc import abstractmethod
from player_action import PlayerAction
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

    def effect(self, user, target):
        user.player_action.heal(2)

    def __repr__(self):
        return f"Apple: {self.description}"


class Cupcake(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.cupcake
        self.description = "Heal 4 HP"

    def effect(self, user, target):
        user.player_action.heal(4)

    def __repr__(self):
        return f"Cupcake: {self.description}"


class Cake(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.cake
        self.description = "Heal half of your lost HP(round down)"

    def effect(self, user, target):
        lost_hp = user.data.max_health - user.data.health
        user.player_action.heal(math.ceil(lost_hp / 2))

    def __repr__(self):
        return f"Cake: {self.description}"


class Muffin(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.muffin
        self.description = "Roll a dice, heal dice number"

    def effect(self, user, target):
        num = user.player_action.roll_dice()
        user.player_action.heal(num)

    def __repr__(self):
        return f"Muffin: {self.description}"


class Sandglass(HealCard):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.identity = HealingIdentity.sandglass
        self.description = "Recover to your last turn's HP"

    def effect(self, user, target):
        if user.data.health < user.data.health_last_turn:
            user.player_action.heal(user.data.health_last_turn - user.data.health)

    def __repr__(self):
        return f"Sandglass: {self.description}"
