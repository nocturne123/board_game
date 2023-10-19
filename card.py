from ENUMS.common_enums import CardTypeEnum, CardStateEnum, DamageTypeEnum
from transitions import Machine
from player import Player
from abc import abstractmethod
from damage import Damage


"""卡牌的状态机实现"""
"""2023.10.13更新，卡牌类现在只有数据，卡牌产生效果的代码进入player_action"""
"""2023.10.18更新，卡牌类现在涉及数据和操作，player_action现在只操作player相关数据，
卡牌自身只提供效果，抽牌、使用、弃牌的操作在card_action中实现"""

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
        "trigger": "cancel_play",
        "source": CardStateEnum.on_use,
        "dest": CardStateEnum.in_hand,
    },
    {
        "trigger": "take_effect",
        "source": CardStateEnum.on_use,
        "dest": CardStateEnum.on_taking_effect,
    },
    {
        "trigger": "end_effect",
        "source": CardStateEnum.on_taking_effect,
        "dest": CardStateEnum.on_discard,
    },
    {
        "trigger": "get_equipped",
        "source": CardStateEnum.on_use,
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


class Card:
    """卡牌的基类，所有摸牌堆里的卡牌继承于此类，注意：卡牌不负责检查目标是否合理，检测目标的行为在player_action中实现"""

    def __init__(
        self,
        card_type: CardTypeEnum,
        states=CardStateEnum,
        transitions=transtions,
    ):
        # 是否有距离限制
        self.distance_limited = True
        # 状态机
        self.machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            initial=CardStateEnum.in_draw_pile,
        )
        # 卡牌类型
        self.card_type = card_type

    @abstractmethod
    def effect(self, user: Player, target: Player):
        """卡牌产生效果"""
        pass

    def __repr__(self) -> str:
        return f"{self.card_type}"


class PhysicalAttackCard(Card):
    """物理攻击牌"""

    def __init__(
        self,
        card_type: CardTypeEnum = CardTypeEnum.physical_attack,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(card_type, states, transitions)
        self.distance_limited = True

    def effect(self, user: Player, target: Player):
        """卡牌产生效果"""
        target.receive_damage(
            Damage(user.data.physical_attack, DamageTypeEnum.physical)
        )

    def __repr__(self) -> str:
        return "PhysicalAttack"


class MagicAttackCard(Card):
    """魔法攻击牌"""

    def __init__(
        self,
        card_type: CardTypeEnum = CardTypeEnum.magic_attack,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(card_type, states, transitions)
        self.distance_limited = True

    def effect(self, user: Player, target: Player):
        """卡牌产生效果"""
        target.receive_damage(Damage(user.data.magic_attack, DamageTypeEnum.magic))

    def __repr__(self) -> str:
        return "MagicAttack"


class MentalAttackCard(Card):
    """心理攻击牌"""

    def __init__(
        self,
        card_type: CardTypeEnum = CardTypeEnum.mental_attack,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(card_type, states, transitions)
        self.distance_limited = True

    def effect(self, user: Player, target: Player):
        """卡牌产生效果"""
        target.receive_damage(Damage(user.data.mental_attack, DamageTypeEnum.mental))

    def __repr__(self) -> str:
        return "MentalAttack"


class StealCard(Card):
    """偷窃牌"""

    def __init__(
        self,
        card_type: CardTypeEnum = CardTypeEnum.steal,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(card_type, states, transitions)
        self.distance_limited = True

    def effect(self, user: Player, target: (Player, Card)):
        """卡牌产生效果"""
        target[1].get_stolen()
        target[0].data.hand_sequence.remove(target[1])
        user.data.hand_sequence.append(target[1])

    def __repr__(self) -> str:
        return "Steal"
