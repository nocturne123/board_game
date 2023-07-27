from player import Player
from card import PhysicalAttackCard
from charaters import Charater
from ENUMS import CardTypeEnum
from pprint import pprint
from game import DrawPile

big_mac = Charater(15, 0, 3, 0, 1)
mac_player = Player(big_mac)

injury_test_dummy = Charater(15, 0, 3, 0, 1)
dummy_player = Player(injury_test_dummy)

physical_attack_card_1 = PhysicalAttackCard()
physical_attack_card_2 = PhysicalAttackCard()
physical_attack_card_3 = PhysicalAttackCard()

mac_player.hand_sequence.extend(
    [physical_attack_card_1, physical_attack_card_2, physical_attack_card_3]
)

pprint(mac_player.hand_sequence)

mac_player.use_card(mac_player.hand_sequence[0], dummy_player)
pprint(mac_player.hand_sequence)
pprint(dummy_player.health)

card_pile1 = DrawPile()
pprint(card_pile1.card_list)
