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

# 装备，这里只导入没有主动技能的装备
from armors import Clothes, Hat, Amulet, Glasses
from weapons import Instrument, Machine

# dummy的简易ai
from dummy_ai import dummy_ai_discard, dummy_ai_play

# mac的交互ui
from mac_player_ui import play_ui, discard_ui

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
# print(mac_player.data.stage_state.state)

# 游戏初始化
game = Game()
game.game_set_gamemode(GameModeEnum.FFA)
game.add_player(mac_player, dummy_player)
game.set_team()

# 初始化牌堆
draw_pile = DrawPile()
discard_pile = DiscardPile()
base_class = [PhysicalAttackCard, MagicAttackCard, MentalAttackCard]
for cls in base_class:
    cards = [cls() for i in range(15)]
    draw_pile.extend(cards)
steal_cards = [StealCard() for i in range(8)]
draw_pile.extend(steal_cards)

# 增加恢复牌，包括蛋糕、杯糕、苹果、松饼各两张
healing_class = [Cake, Cupcake, Apple, Muffin]
for cls in healing_class:
    healings = [cls() for i in range(2)]
    draw_pile.extend(healings)


# 增加装备牌，包括衣服、帽子、护身符、眼镜、乐器、机器各两张
equipment_class = [Clothes, Hat, Amulet, Glasses, Instrument, Machine]
for cls in equipment_class:
    equipments = [cls() for i in range(2)]
    draw_pile.extend(equipments)

# 简单洗个牌
shuffle(draw_pile)

# 游戏增加牌堆
game.game_set_pile(draw_pile, discard_pile)
game.game_start_dealing()
# 根据游戏胜利条件进行的主循环
while game.winning_team():
    game.set_player_to_current()
    game.set_current_player_start_turn()
    if game.current_player == mac_player:
        while mac_player.data.stage_state.state == PlayerStateEnum.play:
            play_ui(mac_player, discard_pile, dummy_player)
        while mac_player.data.stage_state.state == PlayerStateEnum.discard:
            discard_ui(mac_player, discard_pile)
        mac_player.player_action.end_turn()
    elif game.current_player == dummy_player:
        while dummy_player.data.stage_state.state == PlayerStateEnum.play:
            dummy_ai_play(dummy_player, discard_pile, mac_player)
        while dummy_player.data.stage_state.state == PlayerStateEnum.discard:
            dummy_ai_discard(dummy_player, discard_pile)
        dummy_player.player_action.end_turn()
    game.next_team()
print(f"胜利者为{game.alive_team_deque[0]}")
