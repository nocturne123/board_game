from team import Team
from player import Player
from charaters import Charater, SpeciesEnum

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

# 玩家：大麦和dummy
mac_player = Player(big_mac)
dummy_player = Player(dummy)
a = Team(maxlen=1)
a.append(mac_player)
print(a)
