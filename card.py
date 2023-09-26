from ENUMS import CardTypeEnum, CardStateEnum, DamageTypeEnum
import abc

from player_state_machine import Player
from damage import Damage

from transitions import Machine

"""卡牌的状态机实现"""

transtions = [
    {
        "trigger": "get_draw",
        "source": CardStateEnum.in_draw_pile,
        "dest": CardStateEnum.on_draw,
    },
    {
        "trigger": "get_into_hand",
        "source": CardStateEnum.on_draw,
        "dest": CardStateEnum.in_hand,
    },
    {
        "trigger": "get_played",
        "source": CardStateEnum.in_hand,
        "dest": CardStateEnum.on_use,
    },
    {
        "trigger": "choose_target",
        "source": CardStateEnum.on_use,
        "dest": CardStateEnum.on_choose_target,
        "after": "get_target",
    },
    {
        "trigger": "take_effect",
        "source": CardStateEnum.on_choose_target,
        "dest": CardStateEnum.on_taking_effect,
        "after": "on_taking_effect",
    },
    {
        "trigger": "end_effect",
        "source": CardStateEnum.on_taking_effect,
        "dest": CardStateEnum.on_discard,
    },
    {
        "trigger": "get_equipped",
        "source": CardStateEnum.on_choose_target,
        "dest": CardStateEnum.on_equipment,
    },
    {
        "trigger": "get_discarded",
        "source": CardStateEnum.in_hand,
        "dest": CardStateEnum.on_discard,
    },
    {
        "trigger": "get_stolen",
        "source": CardStateEnum.in_hand,
        "dest": CardStateEnum.in_hand,
    },
    {
        "trigger": "get_unmounted",
        "source": CardStateEnum.on_equipment,
        "dest": CardStateEnum.on_discard,
    },
    {
        "trigger": "get_into_discard_pile",
        "source": CardStateEnum.on_discard,
        "dest": CardStateEnum.in_discard_pile,
    },
]


class Card(metaclass=abc.ABCMeta):
    """卡牌的基类，所有摸牌堆里的卡牌继承于此类"""

    def __init__(
        self,
        draw_pile,
        discard_pile,
        card_type: CardTypeEnum,
        states=CardStateEnum,
        transitions=transtions,
    ):
        # 是否有距离限制
        self.distance_limited = True
        self.draw_pile = draw_pile
        self.discard_pile = discard_pile
        self.machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            initial=CardStateEnum.in_draw_pile,
        )
        self.card_type = card_type
        # 弃置后是否自动进入弃牌堆
        self.auto_discard = True
        # 目标
        self.target = None


class PhysicalAttackCard(Card):
    """物理攻击牌"""

    def __init__(
        self,
        draw_pile,
        discard_pile,
        card_type: CardTypeEnum = CardTypeEnum.physical_attack,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(draw_pile, discard_pile, card_type, states, transitions)
        self.distance_limited = True

    def on_taking_effect(self, user: Player):
        """对目标造成物理伤害"""
        self.target.receive_damage(
            Damage(user.physical_attack, DamageTypeEnum.physical)
        )

    def get_target(self, target):
        """选择目标"""
        self.target = target


class MagicAttackCard(Card):
    """魔法攻击牌"""

    def __init__(
        self,
        draw_pile,
        discard_pile,
        card_type: CardTypeEnum = CardTypeEnum.magic_attack,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(draw_pile, discard_pile, card_type, states, transitions)
        self.distance_limited = True

    def on_taking_effect(self, user: Player):
        """对目标造成魔法伤害"""
        self.target.receive_damage(Damage(user.magic_attack, DamageTypeEnum.magic))

    def get_target(self, target):
        """选择目标"""
        self.target = target


class MentalAttackCard(Card):
    """心理攻击牌"""

    def __init__(
        self,
        draw_pile,
        discard_pile,
        card_type: CardTypeEnum = CardTypeEnum.mental_attack,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(draw_pile, discard_pile, card_type, states, transitions)
        self.distance_limited = True

    def on_taking_effect(self, user: Player):
        """对目标造成魔法伤害"""
        self.target.receive_damage(Damage(user.mental_attack, DamageTypeEnum.mental))

    def get_target(self, target):
        """选择目标"""
        self.target = target


if __name__ == "__main__":
    card1 = Card(None, None, CardTypeEnum.magic_attack)

    print(card1.state)
    card1.get_draw()
    print(card1.state)
