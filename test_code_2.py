from ENUMS.common_enums import SpeciesEnum
from player_action import PlayerAction
from base_actions import DecreaseHealth, ReceiveDamage, LivingUpdate, StartTurn, UseCard
from player_data import PlayerData
from charaters import Charater
from damage import DamageTypeEnum, Damage

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

mac_data = PlayerData(big_mac)

A = PlayerAction(mac_data)
A.add_action(DecreaseHealth())
A.add_action(ReceiveDamage())
A.add_action(LivingUpdate())
A.add_action(StartTurn())
A.add_action(UseCard())

print(A.actions)

# 这两步就是一条 [受到伤害 -> 生命值减少 -> 更新生命状态] 的链条
A.add_action_chain(A.actions[1], A.actions[0])
A.add_action_chain(A.actions[0], A.actions[2])
print(A.actions[1])
print(A.actions[1].next_action)

A.actions[1].set_damage(Damage(3, DamageTypeEnum.physical))
print(A.actions[0].decrease_num)

A.chain_of_actions(A.actions[1])

print(A.actions[0].decrease_num)
print(mac_data.health)
