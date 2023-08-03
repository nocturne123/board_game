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

# start_stage函数由game类调用，启动摸牌阶段，玩家进行抽牌，
# 回合结束时调用game类的end_stage,通知game类该阶段以结束
    def start_stage(self, drawpile, player):

        player.draw_card(drawpile)

    def end_stage(self, player, game):
        game.end_stage(self, player)

class UseStage(BaseStage):
    def __init__(self, player):
        super().__init__(player)

    def start_stage(self,player):
        pass

    def end_stage(self,player):
        pass

class DiscardStage(BaseStage):
    def __init__(self, player):
        super().__init__(player)

    def start_stage(self,player):
        if len(player.hand_sequance) <= player.max_hand_sequence:
            pass

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
            player.first_round_draw(self.draw_pile)

# 回合类
class Round:
    def __init__(self,game:Game):
        for player in game.player_list:
            if player.have_draw_card_stage:
                yield DrawStage(player)
            if player.have_use_card_stage:
                yield UseStage(player)
