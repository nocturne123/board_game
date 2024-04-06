"""这个文件是action的实现，action是图论的一部分，起到node的作用"""

from player_data import PlayerData
from abc import abstractmethod
from damage import DamageTypeEnum, Damage
from ENUMS.common_enums import CharaterAliveEnum


class Action:
    def __init__(self, key):
        self.id = key
        self.connectedTo = []

    def __repr__(self) -> str:
        return f"{self.id}"

    @abstractmethod
    def take_action(self):
        pass


class DecreaseHealth(Action):
    def __init__(self, key):
        super().__init__(key)

    def take_action(self, player_data: PlayerData, num: int):
        player_data.health -= num
        return num


class ReceiveDamage(Action):
    def __init__(self, key):
        super().__init__(key)

    def take_action(self, player_data: PlayerData, damage: Damage):
        if damage.type == DamageTypeEnum.physical:
            received_damage = damage.num - player_data.physical_defense
        elif damage.type == DamageTypeEnum.magic:
            received_damage = damage.num - player_data.magic_defense
        elif damage.type == DamageTypeEnum.mental:
            received_damage = damage.num - player_data.mental_defense
        elif damage.type == DamageTypeEnum.real:
            received_damage = damage.num
        # 防止伤害为负数
        if received_damage < 0:
            received_damage = 0

        return received_damage


class LivingUpdate(Action):
    def __init__(self, key):
        super().__init__(key)

    def take_action(self, player_data: PlayerData):
        # 角色眩晕相关的操作后续实现
        # if player_data.colloctions:

        if player_data.health <= 0:
            player_data.living_state = CharaterAliveEnum.dead
        return player_data.living_state


class StartTurn(Action):
    def __init__(self, key):
        super().__init__(key)

    def take_action(self, player_data: PlayerData):
        player_data.turn_count += 1
        return player_data.turn_count
