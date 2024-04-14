"""这个文件是action的实现，action是图论的一部分，起到node的作用"""

from player_data import PlayerData
from abc import abstractmethod
from damage import DamageTypeEnum, Damage
from ENUMS.common_enums import CharaterAliveEnum


class Action:
    def __init__(self) -> None:
        self.next_action = None

    def trigger(self, player_data, extra_function=None):
        if extra_function:
            extra_function(self, player_data)
        else:
            self.take_action(player_data)

    @abstractmethod
    def take_action(self):
        pass

    # 动作在生效前会把下一个动作需要的信息传递过去
    # 这个函数非常灵活，动作链当中的动作，player_data是通过接口传来传去
    # 大部分的动作都涉及到player_data，但除此之外的动作就由这个接口传递给下一个动作
    def imforme_next_action(self, next_action):
        return None


class DecreaseHealth(Action):
    def __init__(self) -> None:
        super().__init__()
        self.decrease_num = 0

    def take_action(self, player_data: PlayerData):
        player_data.health -= self.decrease_num

    def __repr__(self) -> str:
        return f"DecreaseHealth"


class ReceiveDamage(Action):
    def __init__(self) -> None:
        self.damage = None
        self.out_put_num = 0

    def set_damage(self, damage):
        self.damage = damage

    def take_action(self, player_data: PlayerData):
        if self.damage.type == DamageTypeEnum.physical:
            received_damage = self.damage.num - player_data.physical_defense
        elif self.damage.type == DamageTypeEnum.magic:
            received_damage = self.damage.num - player_data.magic_defense
        elif self.damage.type == DamageTypeEnum.mental:
            received_damage = self.damage.num - player_data.mental_defense
        elif self.damage.type == DamageTypeEnum.real:
            received_damage = self.damage.num
        # 防止伤害为负数
        if received_damage < 0:
            received_damage = 0

        self.out_put_num = received_damage

    def imforme_next_action(self, next_action):
        """一般情况下，受到伤害后，下一步就是生命值减少，将减少的数字"""
        next_action.decrease_num = self.out_put_num
        return next_action

    def __repr__(self) -> str:
        return f"ReceiveDamage"


class LivingUpdate(Action):
    def take_action(self, player_data: PlayerData):
        # 角色眩晕相关的操作后续实现
        # if player_data.colloctions:

        if player_data.health <= 0:
            player_data.living_state = CharaterAliveEnum.dead
        return player_data.living_state

    def __repr__(self) -> str:
        return f"LivingUpdate"


class StartTurn(Action):
    def take_action(self, player_data: PlayerData):
        player_data.turn_count += 1
        return player_data.turn_count

    def __repr__(self) -> str:
        return f"StartTurn"


class UseCard(Action):
    def __init__(self) -> None:
        super().__init__()
        self.target = None

    def take_action(self, card):
        card.take_effect(self, self.target)
        return

    def __repr__(self) -> str:
        return f"UseCard"
