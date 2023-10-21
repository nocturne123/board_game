from game import Game
from player import Player
from card_pile import DrawPile, DiscardPile
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard, StealCard
from healings import Muffin
from charaters import Charater
from ENUMS.common_enums import (
    SpeciesEnum,
    GameModeEnum,
    CharaterAliveEnum,
    PlayerStateEnum,
)
import player_action as PlayerAction
from pprint import pprint
from player_exceptions import NoChanceToAttackException
from team import Team
from collections import deque
from random import shuffle

"""这个文件是经过状态机重构后的测试文件"""

# 初始化牌堆
draw_pile = DrawPile()
discard_pile = DiscardPile()
a = [PhysicalAttackCard() for i in range(16)]
b = [MagicAttackCard() for i in range(16)]
c = [MentalAttackCard() for i in range(16)]
draw_pile.extend(a)
draw_pile.extend(b)
draw_pile.extend(c)
shuffle(draw_pile)

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

# 玩家：大麦和dummy初始化
mac_player = Player(big_mac)
dummy_player = Player(dummy)
print(mac_player.data.health)

# 模拟大麦回合开始，只不过一次抽了5张牌
mac_player.player_action.start_turn()
mac_player.player_action.start_turn_init()
mac_player.player_action.start_draw()
mac_player.card_action.draw_card(draw_pile, 5)
mac_player.player_action.start_play()

# 模拟大麦打出一张牌
print(mac_player.data.hand_sequence)
for card in mac_player.data.hand_sequence:
    print(card.state)
mac_player.card_action.use_card(
    mac_player.data.hand_sequence[0], dummy_player, discard_pile
)
print(dummy_player.data.health)
print(discard_pile[0])
print(discard_pile[0].state)

# 模拟大麦偷牌
# 先往抽牌堆里加入一张偷牌，再加入一张马芬恢复牌，大麦抽到偷牌，dummy抽到马芬，大麦再偷马芬
steal_card = StealCard()
muffin = Muffin()
draw_pile.append(steal_card)
draw_pile.append(muffin)
dummy_player.card_action.draw_card(draw_pile, 1)
print(dummy_player.data.hand_sequence)
mac_player.card_action.draw_card(draw_pile, 1)
mac_player.card_action.use_card(
    mac_player.data.hand_sequence[-1],
    (dummy_player, dummy_player.data.hand_sequence[0]),
    discard_pile,
)
print(mac_player.data.hand_sequence[-1])
print(mac_player.data.hand_sequence[-1].state)

# 模拟大麦打出一张马芬
mac_player.player_action.decrease_health(10)
print(mac_player.data.health)
mac_player.card_action.use_card(
    mac_player.data.hand_sequence[-1],
    mac_player,
    discard_pile,
)
print(mac_player.data.health)
