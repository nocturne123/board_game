"""这个文件是test_code_5.py测试文件里dummy使用的简易ai，用来和玩家对战"""
from player import Player
from card import CardTypeEnum
from ENUMS.common_enums import PlayerStateEnum
from ENUMS.heal_card_enums import HealingIdentity


def dummy_ai_play(dummy: Player, discard_pile, mac_player):
    """dummy的出牌ai分4步，第一步，装装备，第二步，根据剩余血量使用对应的恢复牌
    第三步，使用攻击牌，第四步，使用偷牌"""
    # while dummy.data.stage_state == PlayerStateEnum.play:
    # 装装备
    if not dummy.data.armor_slot:
        for card in dummy.data.hand_sequence:
            if card.card_type == CardTypeEnum.armor:
                dummy.card_action.use_card(card, dummy, discard_pile)
                print(f"dummy装备了{card}")

    if not dummy.data.weapon_slot:
        for card in dummy.data.hand_sequence:
            if card.card_type == CardTypeEnum.weapon:
                dummy.card_action.use_card(card, dummy, discard_pile)
                print(f"dummy装备了{card}")

    # 使用恢复牌
    # 使用恢复牌的逻辑要更细腻一些
    # 先看血量缺口，当血量缺口大于等于2小于4时，优先使用苹果，没到这个血量则不用
    # 当血量缺口大于4时，优先使用杯糕，其次使用松饼，最后苹果
    # 当血量小于一半时，优先使用蛋糕，然后松饼，然后蛋糕，最后苹果
    if dummy.data.max_health - dummy.data.health >= 2:
        for card in dummy.data.hand_sequence:
            if card.card_type == CardTypeEnum.healing:
                if card.identity == HealingIdentity.apple:
                    dummy.card_action.use_card(card, dummy, discard_pile)
                    print(f"dummy使用了{card}")
        if dummy.data.max_health - dummy.data.health >= 4:
            for card in dummy.data.hand_sequence:
                if card.card_type == CardTypeEnum.healing:
                    if card.identity == HealingIdentity.cupcake:
                        dummy.card_action.use_card(card, dummy, discard_pile)
                        print(f"dummy使用了{card}")
                        continue
            for card in dummy.data.hand_sequence:
                if card.card_type == CardTypeEnum.healing:
                    if card.identity == HealingIdentity.cake:
                        dummy.card_action.use_card(card, dummy, discard_pile)
                        print(f"dummy使用了{card}")
            if dummy.data.health <= 7:
                for card in dummy.data.hand_sequence:
                    if card.card_type == CardTypeEnum.healing:
                        if card.identity == HealingIdentity.cake:
                            dummy.card_action.use_card(card, dummy, discard_pile)
                            print(f"dummy使用了{card}")

    # 使用攻击牌
    for card in dummy.data.hand_sequence:
        if card.card_type == CardTypeEnum.physical_attack:
            dealed_damage = dummy.card_action.use_card(card, mac_player, discard_pile)
            print(f"dummy使用了{card},造成了{dealed_damage}点伤害")
            break
        elif card.card_type == CardTypeEnum.magic_attack:
            dealed_damage = dummy.card_action.use_card(card, mac_player, discard_pile)
            print(f"dummy使用了{card},造成了{dealed_damage}点伤害")
            break
        elif card.card_type == CardTypeEnum.mental_attack:
            dealed_damage = dummy.card_action.use_card(card, mac_player, discard_pile)
            print(f"dummy使用了{card},造成了{dealed_damage}点伤害")
            break
    # 结束回合
    dummy.player_action.end_play()


def dummy_ai_discard(dummy: Player, discard_pile):
    """dummy的弃牌ai，弃牌直到手牌数量小于等于6，优先弃装备
    然后弃攻击牌，最后弃恢复牌"""
    while len(dummy.data.hand_sequence) > dummy.data.max_hand_sequence_num:
        for card in dummy.data.hand_sequence:
            if card.card_type == CardTypeEnum.armor:
                dummy.card_action.discard_card(card, discard_pile)
                continue
            elif card.card_type == CardTypeEnum.weapon:
                dummy.card_action.discard_card(card, discard_pile)
                continue
        for card in dummy.data.hand_sequence:
            if card.card_type == CardTypeEnum.physical_attack:
                dummy.card_action.discard_card(card, discard_pile)
                continue
            elif card.card_type == CardTypeEnum.magic_attack:
                dummy.card_action.discard_card(card, discard_pile)
                continue
            elif card.card_type == CardTypeEnum.mental_attack:
                dummy.card_action.discard_card(card, discard_pile)
                continue
        for card in dummy.data.hand_sequence:
            if card.card_type == CardTypeEnum.healing:
                dummy.card_action.discard_card(card, discard_pile)

    dummy.player_action.end_discard()
