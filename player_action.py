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
    CardStateEnum,
)
from card_exceptions import NeedTargetException, NeedFurtherTargetException

from player_exceptions import (
    NotInPlayStateException,
    NoChanceToAttackException,
    NeedTargetException,
    NeedFurtherTargetException,
    ImmuneToAttackException,
    ImmuneToStealException,
)
from card_exceptions import NotInHandStateException


def draw_card_from_pile(player: Player, drawpile: DrawPile, num: int = 1):
    """抽牌"""
    for _ in range(num):
        card: Card = drawpile.pop()
        card.get_draw()
        card.get_into_hand()
        player.hand_sequence.append(card)


def player_living_update(player: Player):
    if player.health <= 0:
        player.living_state.die()


def receive_damage(player: Player, damage: Damage):
    """玩家受到伤害"""
    if damage.type == DamageTypeEnum.physical:
        received_damage = damage.num - player.physical_defense
    elif damage.type == DamageTypeEnum.magic:
        received_damage = damage.num - player.magic_defense
    elif damage.type == DamageTypeEnum.mental:
        received_damage = damage.num - player.mental_defense
    player.health -= received_damage
    player_living_update(player)
    return received_damage


def discard_card(player: Player, card: Card, discardpile: DiscardPile):
    """弃牌"""
    player.hand_sequence.remove(card)  # 从手牌中移除
    card.get_discarded()  # 状态切换，in_hand 切换到 on_discard
    discardpile.append(card)  # 加入弃牌堆
    card.get_into_discard_pile()  # 状态切换，on_discard 切换到 in_discard_pile


def choose_card_from_player(user: Player, target: Player, card: Card):
    if card in target.hand_sequence or card in target.equipment_sequence:
        return card


def use_card(
    user: Player,
    card: Card,
    target: Player | Card | None | (Player, Card) = None,
    discard_pile: DiscardPile = None,
):
    """使用卡牌"""
    # TODO:卡牌的出牌逻辑需要大量更新
    try:
        # 检查是否在手牌中，不能打出不在手牌中的牌
        if card.state != CardStateEnum.in_hand:
            raise NotInHandStateException("Card is not in hand")

        # 检查是否在play阶段，不能在play阶段以外的阶段打出牌
        if user.stage_state.is_play() != True:
            raise NotInPlayStateException("Player is not in play stage")

        # 检查是否有攻击次数，没有攻击次数不能打出攻击牌
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            if user.attack_chance_in_turn <= 0:
                card.cancel_play()
                raise NoChanceToAttackException("No attack chance in turn")

        card.get_played()  # 状态切换，in_hand 切换到 on_use

    except NotInPlayStateException:
        print("Please wait until your turn")
    except NeedTargetException:
        print("Card need target")

    else:
        user.hand_sequence.remove(card)  # 从手牌中移除，在使用的最开始已经从手牌中移除了，后续逻辑中不需要再移除

        # 如果使用的是攻击牌，攻击次数减一
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            user.attack_chance_in_turn -= 1

        # 根据不同卡牌类型，进行不同的逻辑
        match card.card_type:
            case CardTypeEnum.physical_attack:  # 物理攻击牌
                if target == None:
                    raise NeedTargetException("Card need target")
                if target.immune_from_attack == True:
                    raise ImmuneToAttackException("Target is immune from attack")
                if isinstance(target, Player):
                    # 所有条件都满足，开始执行卡牌效果
                    card.take_effect()  # 状态切换，on_use 切换到 on_taking_effect
                    target.receive_damage(
                        Damage(user.physical_attack, DamageTypeEnum.physical)
                    )

                    card.end_effect()  # 状态切换，on_taking_effect 切换到 on_discard
                    discard_pile.append(card)  # 加入弃牌堆
                    card.get_into_discard_pile()  # 状态切换，on_discard 切换到 in_discard_pile

                else:
                    raise TypeError("Target is not a player")

            case CardTypeEnum.magic_attack:  # 魔法攻击牌
                if target == None:
                    raise NeedTargetException("Card need target")
                if target.immune_from_attack == True:
                    raise ImmuneToAttackException("Target is immune from attack")
                if isinstance(target, Player):
                    # 所有条件都满足，开始执行卡牌效果
                    card.take_effect()  # 状态切换，on_use 切换到 on_taking_effect
                    target.receive_damage(
                        Damage(user.magic_attack, DamageTypeEnum.magic)
                    )
                    card.end_effect()  # 状态切换，on_taking_effect 切换到 on_discard
                    discard_pile.append(card)  # 加入弃牌堆
                    card.get_into_discard_pile()  # 状态切换，on_discard 切换到 in_discard_pile
                else:
                    raise TypeError("Target is not a player")

            case CardTypeEnum.mental_attack:  # 心理攻击牌
                if target == None:
                    raise NeedTargetException("Card need target")
                if target.immune_from_attack == True:
                    raise ImmuneToAttackException("Target is immune from attack")
                if isinstance(target, Player):
                    # 所有条件都满足，开始执行卡牌效果
                    card.take_effect()  # 状态切换，on_use 切换到 on_taking_effect
                    target.receive_damage(
                        Damage(user.mental_attack, DamageTypeEnum.mental)
                    )
                    card.end_effect()  # 状态切换，on_taking_effect 切换到 on_discard
                    discard_pile.append(card)  # 加入弃牌堆
                    card.get_into_discard_pile()  # 状态切换，on_discard 切换到 in_discard_pile
                else:
                    raise TypeError("Target is not a player")

            case CardTypeEnum.steal:  # 偷窃牌
                if target == None:
                    raise NeedTargetException("Card need target")
                if target[0] == None or target[1] == None:
                    raise NeedFurtherTargetException("Card need further target")
                if target.immune_from_steal == True:
                    raise TypeError("Target is immune from steal")
                if isinstance(target[0], Player) and isinstance(target[1], Card):
                    # 所有条件都满足，开始执行卡牌效果
                    target_player: Player = target[0]
                    target_card: Card = target[1]
                    card.take_effect()  # 状态切换，偷牌卡牌on_use 切换到 on_taking_effect
                    # 卡牌在手牌，则进行偷牌
                    if target_card in target_player.hand_sequence:  # 如果目标牌在目标玩家手牌中
                        target_card.get_stolen()  # 被偷的卡牌进行一次状态切换，in_hand 切换到 in_hand
                        target_player.hand_sequence.remove(target_card)
                        user.hand_sequence.append(target_card)
                        card.end_effect()  # 状态切换，on_taking_effect 切换到 on_discard
                        discard_pile.append(card)
                        card.get_into_discard_pile()
                    # 卡牌在装备区，则进行拆牌
                    elif target_card in target_player.equipment_sequence:
                        target_card.get_unmounted()
                        target_player.equipment_sequence.remove(target_card)
                        target_card.get_into_discard_pile()
                        discard_pile.append(target_card)
                        card.end_effect()  # 状态切换，on_taking_effect 切换到 on_discard
                        discard_pile.append(card)
                        card.get_into_discard_pile()

                else:
                    raise TypeError(
                        "Target Mismatch, this could be a problem with card or player"
                    )


def player_end_play(player: Player):
    """结束回合"""
    if len(player.hand_sequence) <= player.max_hand_sequence_num:
        player.stage_state.skip_discard()
        player.stage_state.end_turn()
    else:
        player.stage_state.end_play()


def player_end_discard(player: Player):
    """结束阶段"""
    player.stage_state.end_discard()


def player_end_turn(player: Player):
    """结束回合"""
    player.stage_state.end_turn()


def player_start_turn_init(player: Player):
    """回合开始时的初始化"""
    player.move_chance_in_turn = player.move_chance
    player.attack_chance_in_turn = player.attack_chance
