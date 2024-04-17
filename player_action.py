"""2024.4.4更新，以图论为数据基础重构,基础的node在base_actions里实现"""

from player_data import PlayerData
from damage import Damage
import random
from ENUMS.common_enums import (
    PlayerStateEnum,
    CharaterAliveEnum,
    SpeciesEnum,
    DamageTypeEnum,
    CardTypeEnum,
    CardStateEnum,
)
from base_actions import (
    Action,
    DecreaseHealth,
    ReceiveDamage,
    LivingUpdate,
    StartDrawState,
    StartPlayState,
    StartDiscardState,
    EndDiscardState,
    DrawCard,
    DiscardCard,
    UseCard,
    Heal,
    RollDice,
    EarthponyRollDice,
)

DEFAUT_ACTIONS = [
    Action,
    DecreaseHealth,
    ReceiveDamage,
    LivingUpdate,
    StartDrawState,
    StartPlayState,
    StartDiscardState,
    EndDiscardState,
    DrawCard,
    DiscardCard,
    UseCard,
    Heal,
    RollDice,
    EarthponyRollDice,
]


class PlayerAction:
    """玩家操作类"""

    def __init__(self, player_data) -> None:
        self.data: PlayerData = player_data
        self.actions = []

        # 玩家动作初始化的时候将默认动作添加进去
        for action in DEFAUT_ACTIONS:
            self.actions.append(action())

    # 这一步其实完全可以用python原本的列表append方法,现在先这样写，防止后续需要对这个函数进行修改
    def add_action(self, action):
        self.actions.append(action)

    def add_action_chain(self, action, next_action):
        action.next_action = next_action

    def chain_of_actions(self, begin_action):
        """执行action链
        如果有下一个动作，将信息传递给下一个动作
        如果没有下一个动作，则链条终止"""

        if begin_action.next_action:
            print(f"{begin_action} has next action")
            begin_action.trigger(self.data)
            begin_action.imforme_next_action(begin_action.next_action)

            self.chain_of_actions(begin_action.next_action)
        else:
            begin_action.trigger(self.data)
