from ENUMS.common_enums import (
    CardTypeEnum,
    CardStateEnum,
    DamageTypeEnum,
    AttackCardTypeEnum,
)
from abc import abstractmethod
from damage import Damage


"""卡牌的状态机实现"""
"""2023.10.13更新，卡牌类现在只有数据，卡牌产生效果的代码进入player_action"""
"""2023.10.18更新，卡牌类现在涉及数据和操作，player_action现在只操作player相关数据，
卡牌自身只提供效果，抽牌、使用、弃牌的操作在card_action中实现"""
"""2024.4.5更新，卡牌调用player_action的方法，实现效果"""


class Card:
    """卡牌的基类，所有摸牌堆里的卡牌继承于此类，注意：卡牌不负责检查目标是否合理，检测目标的行为在player_action中实现"""

    def __init__(
        self,
        card_type: CardTypeEnum,
    ):
        # 是否有距离限制
        self.distance_limited = True

        # 卡牌类型
        self.card_type = card_type

    def use(self, user, targets):
        # 打出卡牌和卡牌生效需要拆分开
        self.effect(user, targets)

    @abstractmethod
    def effect(self, user, targets):
        pass

    def __repr__(self) -> str:
        return f"{self.card_type}"


class AttackCard(Card):
    def __init__(self):
        super().__init__(card_type=CardTypeEnum.attack)


class StealCard(Card):
    """偷窃牌"""

    def __init__(
        self,
        card_type: CardTypeEnum = CardTypeEnum.steal,
    ):
        super().__init__(card_type)
        self.distance_limited = True

    def effect(self, user, target: tuple):
        """卡牌产生效果"""
        match target[1].state:
            case CardStateEnum.on_equipment:
                # TODO：拆装备的逻辑需要重构

                target[0].card_action.unmount_item(target[1])

            case CardStateEnum.in_hand:
                # TODO：偷牌的逻辑需要重构，现有的偷牌只是把手牌从a玩家的手里移到了b玩家的手里
                # 应该是有一个被偷掉的方法，而不是简单的remove，这样方便加相关的hook
                target[1].get_stolen()
                target[0].data.hand_sequence.remove(target[1])
                user.data.hand_sequence.append(target[1])

    def __repr__(self) -> str:
        return "Steal"
