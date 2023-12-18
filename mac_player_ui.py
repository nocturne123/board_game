"""这个文件用于test_code_5.py里面的程序互动，利用print和input实现基础的出牌、弃牌操作"""
from player import Player
from card import CardTypeEnum
from ENUMS.common_enums import PlayerStateEnum
from ENUMS.heal_card_enums import HealingIdentity
import random


# 按i给出对局的基本信息，所有按i的地方都调用这个函数
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


# 因为偷牌涉及到两层的“选择-回退”逻辑，要写两遍match-case，为了避免缩进地狱，
# 把偷牌的逻辑包装成一个函数，后面调用
def steal_helper(mac_player: Player, dummy: Player, discard_pile):
    if len(dummy.data.hand_sequence) == 0 and len(dummy.data.equipment_sequence) == 0:
        print("dummy既没有手牌也没有装备")

    elif len(dummy.data.hand_sequence) == 0:
        print(f"dummy没有手牌，但是有装备，dummy的装备栏为")
        for index, item in enumerate(dummy.data.equipment_sequence):
            print(f"{index}:{item}")
        while key_pressed_4 := input("输入对应的数字拆下装备，输入q退回上级，输入i查看详细信息") != "q":
            if key_pressed_4.isdigit() and int(key_pressed_4) < len(
                dummy.data.equipment_sequence
            ):
                card = mac_player.card_action.use_card(
                    card,
                    (
                        dummy,
                        dummy.data.equipment_sequence[index],
                    ),
                    discard_pile,
                )
                print(f"你使用了{card},偷走了dummy的{dummy.data.equipment_sequence[index]}")
                break
            elif key_pressed_4 == "i":
                print_basic_imformation(mac_player, dummy)
                print("dummy的装备栏为")
                for index, item in enumerate(dummy.data.equipment_sequence):
                    print(f"{index}:{item}")
                print("dummy没有手牌，只能弃置装备")
            else:
                print(f"你的输入是{key_pressed_4}，我不知道这个是啥，再来一次吧")

    elif len(dummy.data.equipment_sequence) == 0:
        while (
            key_pressed_4 := input("dummy没有装备，但是有手牌，按1随机偷取一张牌，按i查看详细信息，按q退回上一级") != "q"
        ):
            match key_pressed_4:
                case "1":
                    card = mac_player.card_action.use_card(
                        card,
                        (
                            dummy,
                            dummy.data.hand_sequence[
                                random.randint(
                                    0,
                                    len(dummy.data.hand_sequence) - 1,
                                )
                            ],
                        ),
                        discard_pile,
                    )
                    break
                case "i":
                    print_basic_imformation(mac_player, dummy)
                    print("dummy没有装备，只能随机偷取一张手牌，按1随机偷取，按q退回上级，按i查看详细信息")
                case _:
                    print(f"你的输入是{key_pressed_4}，我不知道这个是啥，再来一次吧")
    # 接下来是既有手牌也有装备的情况
    else:
        while key_pressed_3 := input("按q退出偷牌，按0随机偷取一张手牌，按1选择一件装备，按i查看当前信息") != "q":
            print(
                f"dummy的手牌数量为{len(dummy.data.hand_sequence)}，dummy的装备栏为{dummy.data.equipment_sequence}"
            )
            match key_pressed_3:
                case "0":
                    card = mac_player.card_action.use_card(
                        card,
                        (
                            dummy,
                            dummy.data.hand_sequence[
                                random.randint(
                                    0,
                                    len(dummy.data.hand_sequence) - 1,
                                )
                            ],
                        ),
                        discard_pile,
                    )
                    print(f"你使用了{card},偷走了dummy的{dummy.data.hand_sequence[0]}")
                    break
                case "1":
                    for index, item in enumerate(dummy.data.equipment_sequence):
                        print(f"{index}:{item}")
                    while (
                        key_pressed_4 := input("输入对应的数字拆下装备，输入q退回上级，输入i查看详细信息") != "q"
                    ):
                        if key_pressed_4.isdigit() and int(key_pressed_4) < len(
                            dummy.data.equipment_sequence
                        ):
                            card = mac_player.card_action.use_card(
                                card,
                                (
                                    dummy,
                                    dummy.data.equipment_sequence[index],
                                ),
                                discard_pile,
                            )
                            print(
                                f"你使用了{card},偷走了dummy的{dummy.data.equipment_sequence[index]}"
                            )
                            break
                        elif key_pressed_4 == "i":
                            print_basic_imformation(mac_player, dummy)
                            print("dummy的装备栏为")
                            for index, item in enumerate(dummy.data.equipment_sequence):
                                print(f"{index}:{item}")

                        else:
                            print(f"你的输入是{key_pressed_4}，我不知道这个是啥，再来一次吧")
                case "i":
                    print_basic_imformation(mac_player, dummy)
                    print(
                        f"dummy的手牌数量为{len(dummy.data.hand_sequence)}，dummy的装备栏为{dummy.data.equipment_sequence}"
                    )


def play_ui(mac_player: Player, discard_pile, dummy: Player):
    # 先把信息都打出来
    print("=" * 30)
    print("-" * 30)
    print(f"你的回合开始了，你抽了{mac_player.data.draw_stage_card_number}张牌")
    print_basic_imformation(mac_player, dummy)

    print("-" * 30)

    # 出牌层级的输入循环
    while (
        key_pressed_1 := input(
            "你可以选择以下操作：\
\n输入1使用手牌，输入2使用角色技能，输入3使用装备技能，输入e进入弃牌阶段，输入i查看当前详细信息"
        )
        != "e"
    ):
        match key_pressed_1:
            # 选牌层级的输入循环
            case "1":
                while key_pressed_2 := input("输入对应的数字打出卡牌，输入q重新选择操作，输入i查看详细信息") != "q":
                    print(f"你的手牌为")
                    for index, card in enumerate(mac_player.data.hand_sequence):
                        print(f"{index}:{card}")
                    print("请输入你要使用的手牌的序号")

                    # 我本来想接着写match、case的，但涉及到一个数字是否在手牌里的判断，还是写if-else了
                    if key_pressed_2.isdigit() and int(key_pressed_2) < len(
                        mac_player.data.hand_sequence
                    ):
                        card = mac_player.data.hand_sequence[int(key_pressed_2)]
                        # 简单捕捉个异常，如果出牌失败就重新选牌
                        try:
                            match card.type:
                                # 攻击牌类因为默认是攻击dummy，选了牌就可以打出去
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
                                    steal_helper(mac_player, dummy, discard_pile)
                                case CardTypeEnum.armor:
                                    mac_player.card_action.use_card(
                                        card, mac_player, discard_pile
                                    )
                                    print(f"你使用了{card}")
                                case CardTypeEnum.weapon:
                                    mac_player.card_action.use_card(
                                        card, mac_player, discard_pile
                                    )
                                    print(f"你使用了{card}")
                                case CardTypeEnum.element:
                                    mac_player.card_action.use_card(
                                        card, mac_player, discard_pile
                                    )
                                    print(f"你使用了{card}")
                                case CardTypeEnum.healing:
                                    mac_player.card_action.use_card(
                                        card, mac_player, discard_pile
                                    )
                                    print(f"你使用了{card}")
                                case _:
                                    print("你使用了未知牌")
                        except Exception as e:
                            print(e)
                            # continue
                    elif key_pressed_2 == "i":
                        print_basic_imformation(mac_player, dummy)
                    else:
                        print(f"你的输入是{key_pressed_2}，我不知道这个是啥，再来一次吧")
                        # continue
            case "2":
                # 角色技能层级的输入循环
                # 因为现在只有一个日光耀耀的技能，所以这里直接选择一张牌给技能用就好了
                while key_pressed_3 := input("现在只有日光耀耀的技能，选择一张牌弃掉，并给dummy上一层印记") != "q":
                    if key_pressed_3.isdigit() and int(key_pressed_3) < len(
                        mac_player.data.hand_sequence
                    ):
                        card = mac_player.data.hand_sequence[int(key_pressed_3)]
                        mac_player.data.character_skills[0].use(
                            card, dummy, discard_pile
                        )

            case "3":
                # 装备技能层级的输入循环
                pass
            case "e":
                # 当输入e的时候已经退出循环了，这里pass就好
                pass
            case "i":
                print_basic_imformation(mac_player, dummy)
                # 这里有一个要不要写continue的问题，现在的功能看是不需要的
                # continue
            case _:
                print(f"你的输入是{key_pressed_1}，我不知道这个是啥，再来一次吧")
                # 同上一条case，这里也有一个需不需要加一个continue的问题
                # continue

    # 输入e后出牌循环结束。进入弃牌阶段或者直接结束
    mac_player.player_action.end_play()
