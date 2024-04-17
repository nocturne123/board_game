"""这个文件是action的实现，action是图论的一部分，起到node的作用"""

from player_data import PlayerData
from abc import abstractmethod
from damage import DamageTypeEnum, Damage
from ENUMS.common_enums import CharaterAliveEnum, PlayerStateEnum
import random
from damage import DamageTypeEnum, Damage


class Action:
    def __init__(self) -> None:
        self.next_action = None

    def trigger(self, player_data, extra_function=None):
        if extra_function:
            extra_function(self, player_data)
        else:
            self.take_action(player_data)
            self.reset_property()

    @abstractmethod
    def take_action(self, player_data: PlayerData):
        pass

    # 动作在生效前会把下一个动作需要的信息传递过去
    # 这个函数非常灵活，动作链当中的动作，player_data是通过接口传来传去
    # 大部分的动作都涉及到player_data，但除此之外的动作就由这个接口传递给下一个动作
    def imform_next_action(self, next_action):
        return None

    # 重置属性，当动作执行完毕，一些被前一个节点修改的属性进行重置
    def reset_property(self):
        pass


class DecreaseHealth(Action):
    """生命值减少，通常下一步更新生命状态"""

    def __init__(self) -> None:
        super().__init__()
        self.decrease_num = 0

    def take_action(self, player_data: PlayerData):
        player_data.health -= self.decrease_num

    def __repr__(self) -> str:
        return f"DecreaseHealth"

    def reset_property(self):
        self.decrease_num = 0


class ReceiveDamage(Action):
    """受到伤害的动作，通常受到伤害的下一步就是生命值减少"""

    def __init__(self) -> None:
        self.damage = None
        self.out_put_num = 0

    def set_damage(self, damage):
        self.damage: Damage = damage

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

    def imform_next_action(self, next_action):
        """一般情况下，受到伤害后，下一步就是生命值减少，将减少的数字"""
        next_action.decrease_num = self.out_put_num
        return next_action

    def __repr__(self) -> str:
        return f"ReceiveDamage"

    def reset_property(self):
        self.damage = None
        self.out_put_num = 0


class LivingUpdate(Action):
    """更新生命状态，通常在生命值减少后或者生命值增加后进行"""

    def take_action(self, player_data: PlayerData):
        # 角色眩晕相关的操作后续实现
        # if player_data.colloctions:

        if player_data.health <= 0:
            player_data.living_state = CharaterAliveEnum.dead
        return

    def __repr__(self) -> str:
        return f"LivingUpdate"


# 以下是几个回合阶段相关的动作
class StartDrawState(Action):
    """回合开始，抽牌阶段，通常下一步动作说就是抽牌，调用抽牌动作时需要告知此次动作为回合开始抽牌"""

    def __init__(self) -> None:
        super().__init__()

    def take_action(self, player_data: PlayerData):
        if player_data.turn_stage == PlayerStateEnum.wait:
            player_data.turn_stage = PlayerStateEnum.draw
            player_data.turn_count += 1
        return

    def __repr__(self) -> str:
        return f"StartTurn"

    # 通常情况下，回合开始后开始抽牌阶段，将抽牌数量告知给抽牌阶段的动作
    def imform_next_action(self, next_action):
        next_action.is_turn_start_draw = True
        return


class StartPlayState(Action):
    """开始出牌阶段"""

    def take_action(self, player_data: PlayerData):
        if player_data.turn_stage == PlayerStateEnum.draw:
            player_data.turn_stage = PlayerStateEnum.play
        return

    def __repr__(self) -> str:
        return f"StartPlayState"


class StartDiscardState(Action):
    """开始弃牌阶段"""

    def take_action(self, player_data: PlayerData):

        if player_data.turn_stage == PlayerStateEnum.play:
            player_data.turn_stage = PlayerStateEnum.discard
        return

    def __repr__(self) -> str:
        return f"Begin Discard"


class EndDiscardState(Action):
    """弃牌阶段结束,回合结束，开始回合外的等待"""

    def take_action(self, player_data: PlayerData):
        if player_data.turn_stage == PlayerStateEnum.discard:
            player_data.turn_stage = PlayerStateEnum.wait
        return

    def __repr__(self) -> str:
        return f"End Discard"


class DrawCard(Action):
    """基础抽牌动作，需要指定抽牌堆，默认情况下抽一张"""

    def __init__(self) -> None:
        super().__init__()
        self.draw_pile = None
        self.num = 1
        self.is_turn_start_draw = False

    # 抽牌默认抽一张
    def take_action(self, player_data: PlayerData):
        if self.is_turn_start_draw:
            self.num = player_data.draw_stage_card_number

        for i in range(self.num):
            card = self.draw_pile.pop()
            card.on_draw(player_data)
            player_data.hand_sequence.append(self.draw_pile.pop())

        return

    def __repr__(self) -> str:
        return f"DrawCard"

    def reset_property(self):
        self.num = 1
        self.draw_pile = None
        self.is_turn_start_draw = False


class DiscardCard(Action):
    def __init__(self) -> None:
        super().__init__()
        self.card = None
        self.discard_pile = None

    def take_action(self, player_data: PlayerData):
        player_data.hand_sequence.remove(self.card)
        self.card.on_discard(player_data)
        self.discard_pile.append(self.card)

    def reset_property(self):
        self.card = None
        self.discard_pile = None


class UseCard(Action):
    def __init__(self) -> None:
        super().__init__()
        self.target = None
        self.card = None

    def take_action(self, player_data):
        self.card.take_effect(player_data, self.target)
        return

    def __repr__(self) -> str:
        return f"UseCard"


class Heal(Action):
    def __init__(self) -> None:
        self.heal_num = 0

    def take_action(self, player_data: PlayerData):
        player_data.health += self.heal_num

    def __repr__(self) -> str:
        return f"Heal"

    def reset_property(self):
        self.heal_num = 0


class RollDice(Action):
    def __init__(self) -> None:
        self.dice_num = 0

    def take_action(self, player_data: PlayerData):
        self.dice_num = random.randint(1, 6)
        return self.dice_num

    def __repr__(self) -> str:
        return f"RollDice"

    def reset_property(self):
        self.dice_num = 0


class EarthponyRollDice(RollDice):
    def __init__(self) -> None:
        super().__init__()

    def take_action(self, player_data: PlayerData):
        super().take_action(player_data)

    def __repr__(self) -> str:
        return f"EarthponyRollDice"
