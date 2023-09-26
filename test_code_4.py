from game import Game
from player_state_machine import Player
from card_pile import DrawPile, DiscardPile
from card_state_machine import PhysicalAttackCard, MagicAttackCard, MentalAttackCard
from charaters_dataclass import Charater, SpeciesEnum

draw_pile = DrawPile()
draw_pile.test_draw_pile()
discard_pile = DiscardPile()

big_mac = Charater(15, 0, 3, 0, 1, "big_mac", (1, 2, 3), SpeciesEnum.earth_pony)
dummy = Charater(15, 0, 3, 0, 1, "dummy", (1, 2, 3), SpeciesEnum.earth_pony)
