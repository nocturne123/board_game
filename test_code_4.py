from game import Game
from player import Player
from card_pile import DrawPile, DiscardPile
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard
from charaters import Charater
from ENUMS import SpeciesEnum, GameModeEnum
from player_action import PlayerAction

"""这个文件是经过状态机重构后的测试文件"""

draw_pile = DrawPile()
draw_pile.test_draw_pile()
discard_pile = DiscardPile()

big_mac = Charater(
    health=15,
    magic_attack=0,
    physical_attack=3,
    mental_attack=0,
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

mac_player = Player(big_mac)
dummy_player = Player(dummy)

game = Game()
game.add_player(mac_player, dummy_player)
game.game_set_gamemode(GameModeEnum.FFA)
game.game_set_pile(draw_pile, discard_pile)

game.set_team()
game.game_start_dealing()

for player in game.player_list:
    player.stage_state_init()

print(mac_player.hand_sequence)

print(mac_player.state)
PlayerAction.draw_card_from_pile(
    draw_pile, mac_player, mac_player.draw_stage_card_number
)
print(mac_player.hand_sequence)
