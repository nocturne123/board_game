from ENUMS.common_enums import CardTypeEnum, CardStateEnum, DamageTypeEnum
from transitions import Machine
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

        # 卡牌的hook函数，分别是卡牌生效前的hook，卡牌生效后的hook，替换卡牌效果的hook,增加效果的hook
        self.hook_before_effect = []
        self.hook_after_effect = []
        self.hook_replace_effect = []
        self.hook_change_effect = []

    def use(self, user, target):
        """卡牌使用，当卡牌生效前的hook不为空时，将self,user,target传入hook函数，
        当卡牌替换的函数不为空时，将self,user,target传入hook函数，否则调用effect函数，
        当卡牌生效后的hook不为空时，将self,user,target传入hook函数"""

        if self.hook_before_effect:
            for func in self.hook_before_effect:
                func(self, user, target)

            # 当全部函数运行完毕后，清空hook_before_effect
            self.hook_before_effect.clear()

        # 有替换函数的情况，这种情况下不调用effect函数
        if self.hook_replace_effect:
            for func in self.hook_replace_effect:
                func(self, user, target)
            self.hook_replace_effect.clear()

        # 没有替换函数，正常运行effect函数，如果有hook_change_effect，将hook传进去
        else:
            # 如果造成伤害了，将伤害值传出去
            if self.hook_change_effect:
                dealed_damage_int = self.effect(user, target, self.hook_change_effect)
            else:
                dealed_damage_int = self.effect(user, target)

            return dealed_damage_int

        if self.hook_after_effect:
            for func in self.hook_after_effect:
                func(self, user, target)
            self.hook_after_effect.clear()

    @abstractmethod
    def effect(self, user, target):
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

    # 这里的hook是一个列表，列表里包装函数，如果hook不为空，则运行里面的函数，
    # hook由card的use方法传参传进来
    def effect(self, user, target, hook=None):
        """卡牌产生效果，如果有额外的hook函数，在构造damage之后调用，修改damage，再对目标传递damage"""
        if hook:
            damage = Damage(user.data.physical_attack, DamageTypeEnum.physical)
            for func in hook:
                func(damage)
            dealed_damage = target.player_action.receive_damage(damage)
            return dealed_damage

        else:
            dealed_damage = target.player_action.receive_damage(
                Damage(user.data.physical_attack, DamageTypeEnum.physical)
            )
            return dealed_damage

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

    def effect(self, user, target, hook=None):
        """卡牌产生效果，如果有额外的hook函数，在构造damage之后调用，修改damage，再对目标传递damage"""
        if hook:
            damage = Damage(user.data.magic_attack, DamageTypeEnum.magic)
            for func in hook:
                func(damage)
            dealed_damage = target.player_action.receive_damage(damage)
            return dealed_damage

        else:
            dealed_damage = target.player_action.receive_damage(
                Damage(user.data.magic_attack, DamageTypeEnum.magic)
            )
            return dealed_damage

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

    def effect(self, user, target, hook=None):
        """卡牌产生效果，如果有额外的hook函数，在构造damage之后调用，修改damage，再对目标传递damage"""
        if hook:
            damage = Damage(user.data.mental_attack, DamageTypeEnum.mental)
            for func in hook:
                func(damage)
            dealed_damage = target.player_action.receive_damage(damage)
            return dealed_damage

        else:
            dealed_damage = target.player_action.receive_damage(
                Damage(user.data.mental_attack, DamageTypeEnum.mental)
            )
            return dealed_damage

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

    def effect(self, user, target: tuple):
        """卡牌产生效果"""
        match target[1].state:
            case CardStateEnum.on_equipment:
                # TODO：拆装备的逻辑需要重构
                target[1].get_unmounted()
                target[0].card_action.unmount_item(target[1])

            case CardStateEnum.in_hand:
                target[1].get_stolen()
                target[0].data.hand_sequence.remove(target[1])
                user.data.hand_sequence.append(target[1])

    def __repr__(self) -> str:
        return "Steal"
