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
print("=" * 30)


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
print("=" * 30)

# 模拟大麦打出一张马芬
mac_player.player_action.decrease_health(9)
print(mac_player.data.health)
mac_player.card_action.use_card(
    mac_player.data.hand_sequence[-1],
    mac_player,
    discard_pile,
)
print(mac_player.data.health)
print("=" * 30)


# 模拟大麦抽到衣服并装上
clothes = Clothes()
draw_pile.append(clothes)
mac_player.card_action.draw_card(draw_pile, 1)
mac_player.card_action.use_card(clothes, mac_player, discard_pile)
print(mac_player.data.physical_defense)
print(mac_player.data.equipment_sequence)
print(mac_player.data.equipment_sequence[0].state)
print(mac_player.data.stage_state.state)
print("=" * 30)

# 模拟大麦弃掉衣服
mac_player.card_action.unmount_item(mac_player.data.equipment_sequence[0], discard_pile)
print(mac_player.data.physical_defense)
print(mac_player.data.equipment_sequence)
print(discard_pile)
print(discard_pile[-1].state)
print("=" * 30)

# 给大麦增加陆马技能，这里手动构造陆马技能，后续会有一个技能构造器
earth_skill_mac = EarthponySkill(mac_player)
print(mac_player.data.species_skills)
print(mac_player.data.Hook_Before_Effect)
print(mac_player.data.hand_sequence)
mac_player.data.attack_chance_in_turn += 3

print(dummy_player.data.health)
mac_player.card_action.use_card(
    mac_player.data.hand_sequence[0], dummy_player, discard_pile
)
print(dummy_player.data.health)
print("=" * 30)

# 给大麦挂接上日光耀耀的1技能
# 给dummy挂上小呆的技能
sunburst_skill = Sunburst_1(mac_player)
derpy_skill = Derpy_1(dummy_player)
mac_player.data.character_skills[0].use(
    card=mac_player.data.hand_sequence[0],
    target=dummy_player,
    discard_pile=discard_pile,
)
print(dummy_player.data.sunburst_mark)

# 再给dummy挂上日光耀耀的技能
sunburst_skill_1 = Sunburst_1(dummy_player)
dummy_player.card_action.draw_card(draw_pile, 5)
dummy_player.data.character_skills[1].use(
    card=dummy_player.data.hand_sequence[0],
    target=mac_player,
    discard_pile=discard_pile,
)

# 没有报错，说明技能计数相互之间不影响，接下来测试使用了两次技能的情况
mac_player.data.character_skills[0].use(
    card=mac_player.data.hand_sequence[0],
    target=dummy_player,
    discard_pile=discard_pile,
)
