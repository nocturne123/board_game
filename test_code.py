from player import Player
from charaters import Charater
from pprint import pprint
from game import DrawPile, Game
from ENUMS import SpeciesEnum

# 这个测试例模拟了大麦和一个木头人对战的情形，game类初始化后为玩家发手牌
# 然后大麦将手里的4张牌全部打出，打在木头人身上

# 大麦
big_mac = Charater(15, 0, 3, 0, 1, "big_mac", SpeciesEnum.earth_pony)
mac_player = Player(big_mac)

# 木头人
injury_test_dummy = Charater(15, 0, 3, 0, 1, "dummy", SpeciesEnum.earth_pony)
dummy_player = Player(injury_test_dummy)


pprint(mac_player.hand_sequence)
test_draw_pile = DrawPile()
test_draw_pile.test_draw_pile()
print(test_draw_pile)

test_game = Game(None, test_draw_pile, mac_player, dummy_player)
test_game.game_start_dealing()
pprint(mac_player.hand_sequence)

for i in range(len(mac_player.hand_sequence)):
    mac_player.use_card(mac_player.hand_sequence[0], dummy_player)
pprint(mac_player.hand_sequence)
pprint(dummy_player.health)
