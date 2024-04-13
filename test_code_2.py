from ENUMS.common_enums import SpeciesEnum
from player_action import PlayerAction
from base_actions import DecreaseHealth, ReceiveDamage, LivingUpdate, StartTurn, UseCard
from player_data import PlayerData
from charaters import Charater

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

A = PlayerAction(big_mac)
A.add_action(DecreaseHealth())
A.add_action(ReceiveDamage())
A.add_action(LivingUpdate())
A.add_action(StartTurn())
A.add_action(UseCard())

print(A.actions)
A.add_action_path(A.actions[0], A.actions[1])
print(A.action_path)
