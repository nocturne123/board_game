from random import shuffle
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard
import abc


# 基础阶段类
class BaseStage(metaclass=abc.ABCMeta):
    def __init__(self, player):
        self.player = player

    @abc.abstractclassmethod
    def start_stage(self, player):
        pass

    @abc.abstractclassmethod
    def end_stage(self, palyer):
        pass


# 摸牌阶段实现
class DrawStage(BaseStage):
    super().__init__()

    def start_stage(self, drawpile, player):
        a = []
        a.append(drawpile.pop())
        a.append(drawpile.pop())
        player.hand_sequence.extend(a)


# 牌堆类
class CardPile:
    def __init__(self):
        self.card_list = []


class DrawPile(CardPile):
    def __init__(self) -> None:
        self.card_list = [
            PhysicalAttackCard(),
            MagicAttackCard(),
            MentalAttackCard(),
        ] * 5
        shuffle(self.card_list)


# 回合类
class Round:
    def __init__(self):
        pass


# 游戏类
class Game:
    def __init__(self, *players):
        self.player_list = [*players]
