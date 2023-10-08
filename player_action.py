from player import Player
from damage import Damage
from card import Card
from card_pile import DrawPile, DiscardPile
from ENUMS import PlayerStateEnum, CharaterAliveEnum, SpeciesEnum, DamageTypeEnum

from player_exceptions import NotInPlayStateException
from card_exceptions import NeedTargetException


class ActionRecord:
    """用于记录下玩家的操作，在什么时候使用了什么卡"""

    pass


class PlayerAction:
    """一些玩家的动作，如抽牌、出牌、弃牌等"""

    @staticmethod
    def draw_card_from_pile(player: Player, drawpile: DrawPile, num: int = 1):
        """抽牌"""
        for _ in range(num):
            card: Card = drawpile.pop()
            card.get_draw()
            card.get_into_hand()
            player.hand_sequence.append(card)

    @staticmethod
    def receive_damage(player: Player, damage: Damage):
        """玩家受到伤害"""
        if damage.type == DamageTypeEnum.physical:
            received_damage = damage.num - player.physical_defense
        elif damage.type == DamageTypeEnum.magic:
            received_damage = damage.num - player.magic_defense
        elif damage.type == DamageTypeEnum.mental:
            received_damage = damage.num - player.mental_defense
        player.health -= received_damage
        return received_damage

    @staticmethod
    def discard_card(discardpile: DiscardPile, player: Player, card: Card):
        """弃牌"""
        pass

    @staticmethod
    def use_card(user: Player, card: Card, target: Player | Card | None = None):
        """出牌"""
        try:
            if target is not None:
                PlayerAction.card_choose_target(card, target)
            if user.is_play() != True:
                raise NotInPlayStateException("Player is not in play stage")
            card.get_played()

        except NotInPlayStateException:
            print("Please wait until your turn")
        except NeedTargetException:
            print("Card need target")
        else:
            card.take_effect(user)

    @staticmethod
    def card_choose_target(card: Card, target: Player | Card):
        """卡牌选择目标，可以是玩家或者卡牌"""
        if card.target is None:
            card.target = target

    @staticmethod
    def card_cancel_target(card: Card):
        """卡牌取消目标"""
        card.target = None

    @staticmethod
    def player_end_play(player: Player):
        """结束回合"""
        player.stage_state.end_play()
