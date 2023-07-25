from player import Player
from card import Card
from charaters import Charater
from ENUMS import CardTypeEnum
from pprint import pprint

big_mac = Charater(15, 0, 3, 0, 1)
mac_player = Player(big_mac)

physical_attack_card_1 = Card(card_type=CardTypeEnum.physical_attack)
physical_attack_card_2 = Card(card_type=CardTypeEnum.physical_attack)
physical_attack_card_3 = Card(card_type=CardTypeEnum.physical_attack)

mac_player.hand_sequence.extend([physical_attack_card_1,physical_attack_card_2,physical_attack_card_3])

pprint(mac_player.hand_sequence)