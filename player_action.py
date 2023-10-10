from player import Player
from damage import Damage
from card import Card
from card_pile import DrawPile, DiscardPile
from ENUMS import (
    PlayerStateEnum,
    CharaterAliveEnum,
    SpeciesEnum,
    DamageTypeEnum,
    CardTypeEnum,
)

from player_exceptions import NotInPlayStateException, NoChanceToAttackException
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
    def discard_card(player: Player, card: Card, discardpile: DiscardPile):
        """弃牌"""
        player.hand_sequence.remove(card)
        card.get_discarded()
        discardpile.append(card)
        card.get_into_discard_pile()

    @staticmethod
    def use_card(user: Player, card: Card, target: Player | Card | None = None):
        """出牌"""
        try:
            if target is not None:
                PlayerAction.card_choose_target(card, target)
            if user.is_play() != True:
                raise NotInPlayStateException("Player is not in play stage")
            if (
                card.card_type
                == CardTypeEnum.physical_attack
                | CardTypeEnum.magic_attack
                | CardTypeEnum.mental_attack
            ):
                if user.attack_chance_in_turn <= 0:
                    raise NoChanceToAttackException("No attack chance in turn")
            card.get_played()

        except NotInPlayStateException:
            print("Please wait until your turn")
        except NeedTargetException:
            print("Card need target")
        else:
            if (
                card.card_type
                == CardTypeEnum.physical_attack
                | CardTypeEnum.magic_attack
                | CardTypeEnum.mental_attack
            ):
                user.attack_chance_in_turn -= 1
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
        if len(player.hand_sequence) <= player.max_hand_sequence_num:
            player.stage_state.skip_discard()
            player.stage_state.end_turn()
        else:
            player.stage_state.end_play()

    @staticmethod
    def player_end_discard(player: Player):
        """结束阶段"""
        player.stage_state.end_discard()

    @staticmethod
    def player_end_turn(player: Player):
        """结束回合"""
        player.stage_state.end_turn()

    @staticmethod
    def player_start_turn_init(player: Player):
        """回合开始时的初始化"""
        player.move_chance_in_turn = player.move_chance
        player.attack_chance_in_turn = player.attack_chance
        player.stage_state.start_turn()

    def check_health(player: Player):
        if player.health <= 0:
            player.living_state.die()
