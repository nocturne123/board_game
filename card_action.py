"""这个文件是卡牌的上级操作文件，包括抽牌、卡牌的使用、弃牌等卡牌自己看不到的操作"""
from card import Card
from player import Player
from card_pile import CardPile, DiscardPile, DrawPile


class CardAction:
    def __init__(self, player) -> None:
        self.player: Player = player

    def player_draw_card(self, card_pile: CardPile, num=1):
        """玩家抽牌"""
        for i in range(num):
            card = card_pile.pop()
            card.get_draw()
            card.get_into_hand()
            self.player.hand_sequence.append(card)

    def player_discard_card(self, card: Card, discard_pile: DiscardPile):
        """玩家弃牌"""
        card.get_discarded()
        self.player.hand_sequence.remove(card)
        card.get_into_discard_pile()
        discard_pile.append(card)

    def player_use_card(
        self, card: Card, target: Player | Card | (Player, Card) | None
    ):
        """玩家使用卡牌"""
        card.get_played()
        self.player.hand_sequence.remove(card)
        card.take_effect()
        card.use(self.player, target)
        card.get_into_discard_pile()
        self.player.discard_pile.append(card)
