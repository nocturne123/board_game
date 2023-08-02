from player import Player
from card import PhysicalAttackCard
from charaters import Charater
from ENUMS import CardTypeEnum
from pprint import pprint
from game import DrawPile,Game

big_mac = Charater(15, 0, 3, 0, 1)
mac_player = Player(big_mac)

injury_test_dummy = Charater(15, 0, 3, 0, 1)
dummy_player = Player(injury_test_dummy)


pprint(mac_player.hand_sequence)
test_draw_pile = DrawPile()
test_draw_pile.test_draw_pile()
print(test_draw_pile)

test_game = Game(None,test_draw_pile,mac_player,dummy_player)
test_game.game_start_dealing()
pprint(mac_player.hand_sequence)

for i in range(len(mac_player.hand_sequence)):
    mac_player.use_card(mac_player.hand_sequence[0], dummy_player)
pprint(mac_player.hand_sequence)
pprint(dummy_player.health)

