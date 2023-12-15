from game import Game
from player import Player
from card_pile import DrawPile, DiscardPile
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard, StealCard
from healings import Muffin, Cake
from charaters import Charater
from ENUMS.common_enums import (
    SpeciesEnum,
    GameModeEnum,
    CharaterAliveEnum,
    PlayerStateEnum,
)
from pprint import pprint
from player_exceptions import NoChanceToAttackException
from team import Team
from collections import deque
import random
from random import shuffle
from armors import Clothes, Hat
from species_skills import EarthponySkill

# 技能的测试
from unicorn_skills import Sunburst_1
from pegasus_skills import Derpy_1

# 恢复牌
from healings import Muffin, Cake, Cupcake, Apple

# dummy的简易ai
from dummy_ai import dummy_ai_discard, dummy_ai_play

# 设置随机数种子
random.seed(0)

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

# 游戏初始化
game = Game()
game.game_set_gamemode(GameModeEnum.FFA)
game.add_player(mac_player, dummy_player)
game.set_team()

# 初始化牌堆
draw_pile = DrawPile()
discard_pile = DiscardPile()
physical_attack_cards = [PhysicalAttackCard() for i in range(15)]
magic_attack_cards = [MagicAttackCard() for i in range(15)]
mental_attack_cards = [MentalAttackCard() for i in range(15)]
draw_pile.extend(physical_attack_cards)
draw_pile.extend(magic_attack_cards)
draw_pile.extend(mental_attack_cards)

# 增加恢复牌，包括蛋糕两张、杯糕两张、苹果两张、松饼两张
cakes = [Cake() for i in range(2)]
cupcakes = [Cupcake() for i in range(2)]
apples = [Apple() for i in range(2)]
muffins = [Muffin() for i in range(2)]
draw_pile.extend(cakes)
draw_pile.extend(cupcakes)
draw_pile.extend(apples)
draw_pile.extend(muffins)

# 简单洗个牌
shuffle(draw_pile)

# 游戏增加牌堆
game.game_set_pile(draw_pile, discard_pile)

# 根据游戏胜利条件进行的主循环
while game.winning_team():
    # dummy先出手
    game.set_player_to_current()
    game.set_current_player_start_turn()
