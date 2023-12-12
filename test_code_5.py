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
from random import shuffle
from armors import Clothes, Hat
from species_skills import EarthponySkill

# 技能的测试
from unicorn_skills import Sunburst_1
from pegasus_skills import Derpy_1

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
a = [PhysicalAttackCard() for i in range(16)]
b = [MagicAttackCard() for i in range(16)]
c = [MentalAttackCard() for i in range(16)]
draw_pile.extend(a)
draw_pile.extend(b)
draw_pile.extend(c)
shuffle(draw_pile)

# 游戏增加牌堆
game.game_set_pile(draw_pile, discard_pile)
