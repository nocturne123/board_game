from random import shuffle
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard
import abc


# 基础阶段类
class BaseStage(metaclass=abc.ABCMeta):
    def __init__(self, player):
        self.player = player

    @abc.abstractclassmethod
    def start_stage(self, player, game):
        pass

    @abc.abstractclassmethod
    def end_stage(self, player, game):
        pass


# 摸牌阶段实现
class DrawStage(BaseStage):
    def __init__(self, player):
        super().__init__(player)

# start_stage函数由game类调用，启动摸牌阶段，回合结束时调用game类的end_stage,通知game类该阶段以结束
    def start_stage(self, drawpile, player):

        a = []
        for i in range(player.draw_stage_card_number):
            a.append(drawpile.pop())
        player.hand_sequence.extend(a)

    def end_stage(self, player, game):
        game.end_stage(self, player)


# 牌堆类
class CardPile(list):
    pass


class DrawPile(CardPile):
    

    def test_draw_pile(self):
        self .extend( [
            PhysicalAttackCard(),
            MagicAttackCard(),
            MentalAttackCard(),
        ] * 5)
        shuffle(self)


# 回合类
class Round:
    def __init__(self):
        pass


# 游戏类
class Game:
    def __init__(self, map, draw_pile, *players):
        self.player_list = [*players]
        self.draw_pile = draw_pile
        self.map = map

    def start_stage(self, stage, player):
        pass

    def end_stage(self, stage, player):
        pass

    def game_start_dealing(self):
        for player in self.player_list:
            a=[]
            for i in range(player.start_game_draw):
                a.append(self.draw_pile.pop())
            player.hand_sequence.extend(a)
