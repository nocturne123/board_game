"""这个文件是卡牌的上级操作文件，包括抽牌、卡牌的使用、弃牌等卡牌自己看不到的操作"""
from player_action import PlayerAction
from player_data import PlayerData
from card_pile import DiscardPile, DrawPile
from ENUMS.common_enums import CardTypeEnum, CardStateEnum, PlayerStateEnum
from player_exceptions import (
    NotInPlayStateException,
    NoChanceToAttackException,
    ImmuneToAttackException,
    ImmuneToStealException,
)

from card_exceptions import (
    CardNotInHandStateException,
    CardNotInHandException,
    MismatchedCardException,
)


class CardAction:
    def __init__(self, player_action):
        self.player_action: PlayerAction = player_action
        self.data: PlayerData = player_action.data

        self.Hook_Before_Use = []
        self.Hook_After_Use = []

    def draw_card(self, card_pile: DrawPile, num=1):
        """玩家抽牌"""
        for i in range(num):
            card = card_pile.pop()
            card.get_draw()
            card.get_into_hand()
            self.data.hand_sequence.append(card)

    def discard_card(self, card, discard_pile: DiscardPile):
        """玩家弃牌"""
        card.get_discarded()
        self.data.hand_sequence.remove(card)
        card.get_into_discard_pile()
        discard_pile.append(card)

    def use_card_checker(self, card, target):
        """检查卡牌是否合法"""
        # 检查玩家状态，只有在play状态下才能打出卡牌
        if self.data.stage_state.state != PlayerStateEnum.play:
            raise NotInPlayStateException
        # 检查卡牌是否在状态，你不能打出一张不在手牌状态的卡牌
        if card.state != CardStateEnum.in_hand:
            raise CardNotInHandStateException

        # 你不能打出一张不在手牌中的手牌
        if card not in self.data.hand_sequence:
            raise CardNotInHandException

        # 攻击牌下的检查
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            # 没有攻击次数时不能打出攻击牌
            if self.data.attack_chance_in_turn <= 0:
                raise NoChanceToAttackException
            # 目标免疫攻击时不能打出攻击牌
            if target.data.immune_from_attack:
                raise ImmuneToAttackException

        # 偷窃牌下的检查，目标免疫偷牌时无效
        # 注：target(Player,Card)，Player是被偷牌的目标，Card是被偷的牌
        if card.card_type == CardTypeEnum.steal:
            if target[0].data.immune_from_steal:
                raise ImmuneToStealException
            if (
                target[1] not in target[0].data.equipment_sequence
                and target[1] not in target[0].data.hand_sequence
            ):
                raise MismatchedCardException

    def use_card(
        self,
        card,
        target,  # 摆烂了，target可以为player，也可以是一个tuple[Player,Card]，如果想要类型提示的话一定会import player，但是这样就循环import了
        discard_pile: DiscardPile,
    ):
        """玩家使用卡牌，这个环节要包含卡牌的状态转换、卡牌的位置转换。
        卡牌自己产生的效果在卡牌的effect函数中实现，这里只调用effect函数，不关心效果的具体实现"""
        self.use_card_checker(card, target)  # 检查卡牌是否合法

        # 使用卡牌前的钩子函数
        if self.Hook_Before_Use:
            for func in self.Hook_Before_Use:
                func(self.data, card, target, discard_pile)
        card.get_played()
        self.data.hand_sequence.remove(card)  # 这个时刻，卡牌已经不在手牌中了

        # 当卡牌类型为攻击时，玩家的攻击次数减少1
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            self.data.attack_chance_in_turn -= 1

        # 当卡牌类型为装备时，状态转换逻辑要分开
        if (
            card.card_type == CardTypeEnum.armor
            or card.card_type == CardTypeEnum.weapon
            or card.card_type == CardTypeEnum.element
            or card.card_type == CardTypeEnum.anti_element
        ):
            card.get_equipped()  # 装备卡牌的状态转换，由on_use转换到on_equipment
            self.data.equipment_sequence.append(card)
            card.use(self, target)
            match card.card_type:
                case CardTypeEnum.armor:
                    self.data.armor_slot = True
                case CardTypeEnum.weapon:
                    self.data.weapon_slot = True
                case CardTypeEnum.element, CardTypeEnum.anti_element:
                    self.data.element_slot = True

        else:  # 一般卡牌的状态转换逻辑
            card.take_effect()  # 卡牌的状态转换，由on_use转换到on_taking_effect
            card.use(self, target)
            card.end_effect()  # 卡牌的状态转换，由on_taking_effect转换到on_discard
            card.get_into_discard_pile()  # 卡牌的状态转换，由on_discard转换到in_discard_pile
            discard_pile.append(card)

    def unmount_item(self, card, discard_pile: DiscardPile):
        """玩家卸下物品"""
        card.get_unmounted()  # 物品的状态转换，由on_equipment转换到on_discard
        card.unequiped(self)  # 调用卡牌的unequip函数，进行一些注销的操作
        self.data.equipment_sequence.remove(card)
        match card.card_type:
            case CardTypeEnum.armor:
                self.data.armor_slot = False
            case CardTypeEnum.weapon:
                self.data.weapon_slot = False
            case CardTypeEnum.element, CardTypeEnum.anti_element:
                self.data.element_slot = False
        card.get_into_discard_pile()
        discard_pile.append(card)
