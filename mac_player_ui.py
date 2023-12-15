"""这个文件用于test_code_5.py里面的程序互动，利用print和input实现基础的出牌、弃牌操作"""
from player import Player
from card import CardTypeEnum
from ENUMS.common_enums import PlayerStateEnum
from ENUMS.heal_card_enums import HealingIdentity


def print_basic_imformation(mac_player: Player, dummy: Player):
    print(f"你的生命值为{mac_player.data.health}，最大生命值为{mac_player.data.max_health}")
    print(f"你的角色技能为{mac_player.data.character_skills}")
    print(f"你的种族技能为{mac_player.data.species_skills}")
    print("-" * 30)
    print(f"你的装备栏为{mac_player.data.equipment_sequence}")
    print(f"你的装备技能为{mac_player.data.equipment_skills}")
    print("-" * 30)
    print(f"dummy的生命值为{dummy.data.health}，最大生命值为{dummy.data.max_health}")
    print(f"dummy的手牌数量为{len(dummy.data.hand_sequence)}")
    print(f"dummy的装备栏为{dummy.data.equipment_sequence}")
    print("-" * 30)
    print(f"你的手牌为{mac_player.data.hand_sequence}")
    print("你可以选择以下操作：输入1使用手牌，输入2使用角色技能，输入3使用装备技能，输入q进入弃牌阶段")


def play_ui(mac_player: Player, discard_pile, dummy: Player):
    # 先把信息都打出来
    print("=" * 30)
    print("-" * 30)
    print(f"你的回合开始了，你抽了{mac_player.data.draw_stage_card_number}张牌")
    print_basic_imformation(mac_player, dummy)
    print("-" * 30)

    while input() != "q":
        if input() == "1":
            print(f"你的手牌为")
            for index, card in enumerate(mac_player.data.hand_sequence):
                print(f"{index}:{card}")
            print("请输入你要使用的手牌的序号")
            index = int(input())
            card = mac_player.data.hand_sequence[index]
            match card.type:
                case CardTypeEnum.physical_attack:
                    dealed_damage = mac_player.card_action.use_card(
                        card, dummy, discard_pile
                    )
                    print(f"你使用了{card},造成了{dealed_damage}点伤害")
                case CardTypeEnum.magic_attack:
                    dealed_damage = mac_player.card_action.use_card(
                        card, dummy, discard_pile
                    )
                    print(f"你使用了{card},造成了{dealed_damage}点伤害")
                case CardTypeEnum.mental_attack:
                    dealed_damage = mac_player.card_action.use_card(
                        card, dummy, discard_pile
                    )
                    print(f"你使用了{card},造成了{dealed_damage}点伤害")
                case CardTypeEnum.steal:
                    mac_player.card_action.use_card(
                        card, (dummy, dummy.data.hand_sequence[0]), discard_pile
                    )
                    print(f"你使用了{card},偷走了dummy的{dummy.data.hand_sequence[0]}")
                case CardTypeEnum.armor:
                    mac_player.card_action.use_card(card, mac_player, discard_pile)
                    print(f"你使用了{card}")
                case CardTypeEnum.weapon:
                    mac_player.card_action.use_card(card, mac_player, discard_pile)
                    print(f"你使用了{card}")
                case CardTypeEnum.element:
                    mac_player.card_action.use_card(card, mac_player, discard_pile)
                    print(f"你使用了{card}")
                case CardTypeEnum.healing:
                    mac_player.card_action.use_card(card, mac_player, discard_pile)
                    print(f"你使用了{card}")
                case _:
                    print("你使用了未知牌")
