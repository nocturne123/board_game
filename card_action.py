"""这个文件是卡牌的上级操作文件，包括抽牌、卡牌的使用、弃牌等卡牌自己看不到的操作"""
from card import Card
from player import Player
from card_pile import CardPile, DiscardPile, DrawPile
from ENUMS.common_enums import CardTypeEnum


class CardAction:
    def __init__(self, player) -> None:
        self.player: Player = player

    def draw_card(self, card_pile: CardPile, num=1):
        """玩家抽牌"""
        for i in range(num):
            card = card_pile.pop()
            card.get_draw()
            card.get_into_hand()
            self.player.hand_sequence.append(card)

    def discard_card(self, card: Card, discard_pile: DiscardPile):
        """玩家弃牌"""
        card.get_discarded()
        self.player.hand_sequence.remove(card)
        card.get_into_discard_pile()
        discard_pile.append(card)

    def use_card(
        self,
        card: Card,
        target: Player | Card | (Player, Card) | None,
        discard_pile: DiscardPile,
    ):
        """玩家使用卡牌，这个环节要包含卡牌的状态转换、卡牌的位置转换。
        卡牌自己产生的效果在卡牌的effect函数中实现，这里只调用effect函数，不关心效果的具体实现"""
        card.get_played()
        self.player.hand_sequence.remove(card)  # 这个时刻，卡牌已经不在手牌中了

        # 当卡牌类型为攻击时，玩家的攻击次数减少1
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            self.player.attack_chance_in_turn -= 1

        # 当卡牌类型为装备时，状态转换逻辑要分开
        if (
            card.card_type == CardTypeEnum.armor
            or card.card_type == CardTypeEnum.weapon
            or card.card_type == CardTypeEnum.element
            or card.card_type == CardTypeEnum.anti_element
        ):
            card.get_equipped()  # 装备卡牌的状态转换，由on_use转换到on_equipment
            self.player.data.equipment_sequence.append(card)
            card.effect(self.player, target)
            match card.card_type:
                case CardTypeEnum.armor:
                    self.player.data.armor_slot = True
                case CardTypeEnum.weapon:
                    self.player.data.weapon_slot = True
                case CardTypeEnum.element, CardTypeEnum.anti_element:
                    self.player.data.element_slot = True

        else:  # 一般卡牌的状态转换逻辑
            card.take_effect()  # 卡牌的状态转换，由on_use转换到on_taking_effect
            card.effect(self.player, target)
            card.end_effect()  # 卡牌的状态转换，由on_taking_effect转换到on_discard
            card.get_into_discard_pile()  # 卡牌的状态转换，由on_discard转换到in_discard_pile
            discard_pile.append(card)
