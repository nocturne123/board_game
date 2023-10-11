from game import Game
from player import Player
from card_pile import DrawPile, DiscardPile
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard
from charaters import Charater
from ENUMS import SpeciesEnum, GameModeEnum, CharaterAliveEnum, PlayerStateEnum
from player_action import PlayerAction
from pprint import pprint
from player_exceptions import NoChanceToAttackException
from team import Team
from collections import deque

"""这个文件是经过状态机重构后的测试文件"""

# 初始化牌堆
draw_pile = DrawPile()
draw_pile.test_draw_pile()
discard_pile = DiscardPile()

# 角色：大麦和dummy
big_mac = Charater(
    health=15,
    magic_attack=0,
    physical_attack=3,
    mental_attack=2,
    speed=1,
    name="big_mac",
    collect_items=(1, 2, 3),
    species=SpeciesEnum.earth_pony,
)

dummy = Charater(
    health=15,
    magic_attack=0,
    physical_attack=3,
    mental_attack=0,
    speed=1,
    name="dummy",
    collect_items=(1, 2, 3),
    species=SpeciesEnum.earth_pony,
)

# 玩家：大麦和dummy
mac_player = Player(big_mac)
dummy_player = Player(dummy)
print(mac_player)

# 游戏基础组装
game = Game()
game.add_player(mac_player, dummy_player)
game.game_set_gamemode(GameModeEnum.FFA)
game.game_set_pile(draw_pile, discard_pile)


# 分队，注：这里有问题，我写出来的Team，里面有一个None，但是我不知道为什么
# 这里不适用set_team了，因为set_team里面有shuffle，会打乱顺序，这里直接手动设置
# game.set_team()
game.team_deque = deque()
print(game.team_deque)

team1 = Team(maxlen=1)
team1.append(mac_player)
team2 = Team(maxlen=1)
team2.append(dummy_player)

game.team_deque.append(team1)
game.team_deque.append(team2)

# 可以看见None
print(game.team_deque)

# 初始抽牌，每人抽4张
game.game_start_dealing()

# 初始玩家的状态机
for player in game.player_list:
    player.stage_state_init()
    player.living_state_init()

print(mac_player.stage_state.state)
print(mac_player.living_state.state)
print(dummy_player.stage_state.state)
print(dummy_player.living_state.state)


# 大循环，根据mac_player的状态来判断是否继续，循环内部进行dummy_player的操作和Team类的轮换、活动玩家的轮换
while (
    mac_player.living_state.state == CharaterAliveEnum.alive
    and dummy_player.living_state.state == CharaterAliveEnum.alive
):
    game.set_player_to_current()
    print(f"当前玩家为{game.current_player.name}")
    game.set_current_player_start_turn()
    print(f"当前玩家的状态为{game.current_player.stage_state.state}")
    print(f"大麦的回合开始了")
    print("-" * 50)
    # mac_player的回合，mac先出手，当mac_player的状态为play时，进行出牌操作，出牌操作为内部小循环
    while mac_player.stage_state.state == PlayerStateEnum.play:
        print(f"大麦的出牌阶段开始了")
        print(
            f"你的物理攻击、心理攻击、魔法攻击分别为为{mac_player.physical_attack}|{mac_player.mental_attack}|{mac_player.magic_attack}"
        )
        print(f"你的生命值为{mac_player.health}")
        print(
            f"你的手牌为{[i for i in enumerate(mac_player.hand_sequence)]}，手牌总数为{len(mac_player.hand_sequence)}"
        )
        print("请输入手牌对应的序号，出牌。按q结束回合，进入弃牌阶段")
        while True:
            a = input()
            if a == "q":
                game.current_player.stage_state.end_play()
                break

            if a.isdigit():
                card = mac_player.hand_sequence[int(a)]
                try:
                    PlayerAction.use_card(mac_player, card, target=dummy_player)
                    print(f"你对{dummy_player.name}使用了{card}")
                    print(f"{dummy_player.name}的生命值为{dummy_player.health}")
                    PlayerAction.check_health(dummy_player)
                except NoChanceToAttackException:
                    print("你没有攻击次数了,考虑到我现在没有写别的卡牌，我建议你直接按q结束回合")

    print(f"大麦的出牌阶段结束了")
    print()
    print("-" * 50)
    print()

    while mac_player.stage_state.state == PlayerStateEnum.discard:
        print("进入弃牌阶段")
        while len(mac_player.hand_sequence) > mac_player.max_hand_sequence_num:
            print("请输入你要弃掉的手牌的序号，按q结束弃牌阶段")
            print(
                f"你的手牌为{[i for i in enumerate(mac_player.hand_sequence)]}，手牌总数为{len(mac_player.hand_sequence)}"
            )
            a = input()
            if a.isdigit():
                card = mac_player.hand_sequence[int(a)]
                PlayerAction.discard_card(mac_player, card, game.discard_pile)
                print(f"你弃掉了{card}")
        game.current_player.stage_state.end_discard()
        game.current_player.stage_state.end_turn()

    print()
    print("弃牌阶段结束")
    print()
    print(f"大麦的回合结束了")
    print("弃牌堆里面")
    pprint(game.discard_pile)
    print("-" * 50)
    game.next_team()
    game.set_player_to_current()
    print(f"当前玩家为{game.current_player.name}")
    game.set_current_player_start_turn()
    print(f"{game.current_player.name}的回合开始了，他的生命值为{game.current_player.health}")
    PlayerAction.use_card(
        game.current_player, game.current_player.hand_sequence[0], target=mac_player
    )
    PlayerAction.check_health(mac_player)
    print(
        f"{game.current_player.name}对{mac_player.name}使用了{game.current_player.hand_sequence[0]}"
    )
    print(f"{mac_player.name}的生命值为{mac_player.health}")
    PlayerAction.player_end_play(game.current_player)
    if game.current_player.stage_state.state == PlayerStateEnum.discard:
        PlayerAction.discard_card(
            game.current_player, game.current_player.hand_sequence[0], game.discard_pile
        )
    print(f"{game.current_player.name}的回合结束了")
    print("=" * 50)
    game.next_team()

if mac_player.living_state != CharaterAliveEnum.dead:
    print("大麦赢了")
else:
    print("dummy赢了")
