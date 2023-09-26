from player import Player
from damage import Damage
from card import Card
from card_pile import DrawPile, DiscardPile
from ENUMS import PlayerStateEnum, CharaterAliveEnum, SpeciesEnum, DamageTypeEnum


class PlayerAction:
    """一些玩家的动作，如抽牌、出牌、弃牌等"""

    @staticmethod
    def draw_card_from_pile(drawpile: DrawPile, player: Player, num: int = 1):
        """抽牌"""
        for _ in range(num):
            player.hand_sequance.append(drawpile.pop())

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
