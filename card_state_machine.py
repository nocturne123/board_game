from ENUMS import CardTypeEnum, CardStateEnum
import abc
from player import Player

from transitions import Machine

"""卡牌的状态机实现"""

transtions = [{}]


class Card(metaclass=abc.ABCMeta):
    """卡牌的基类，所有摸牌堆里的卡牌继承于此类"""

    def __init__(self, draw_pile, discard_pile, card_type: CardTypeEnum):
        self.distance_limited = True
        self.draw_pile = draw_pile
        self.discard_pile = discard_pile
        self.state_machine = None
        self.card_type = card_type
