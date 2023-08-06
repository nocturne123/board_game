from random import shuffle
from card import PhysicalAttackCard, MagicAttackCard, MentalAttackCard
import abc
from player import Player


# 阶段在结束时返回一个表示符，使turn类进入下一个阶段，类似的turn结束后返回一个表示符，使round进入下一个阶段
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
    # 玩家回合结束时通知game类
    # 回合开始由game类主导开启回合，回合结束由player主导结束
    # 回合结束时调用game类的end_stage,通知game类该阶段以结束

    # 现阶段的轮次由turn类主持
    def start_stage(self, drawpile, player: Player):
        player.draw_card(drawpile, num=player.draw_stage_card_number)

    def end_stage(self, player, turn):
        turn.end_stage(self, player)


class UseStage(BaseStage):
    def __init__(self, player):
        super().__init__(player)

    def start_stage(self, player: Player):
        player.able_to_use_card = True
        player.able_to_equip = True

    def end_stage(self, player: Player):
        player.able_to_use_card = False
        player.able_to_equip = False


class DiscardStage(BaseStage):
    def __init__(self, player):
        super().__init__(player)

    def start_stage(self, player: Player):
        while len(player.hand_sequance) <= player.max_hand_sequence:
            print(f"你的手牌数大于{player.max_hand_sequence}，请弃牌")


# 牌堆类
class CardPile(list):
    def __init__(self):
        super().__init__()


class DrawPile(CardPile):
    def __init__(self):
        super().__init__()

    def test_draw_pile(self):
        self.extend(
            [
                PhysicalAttackCard(),
                MagicAttackCard(),
                MentalAttackCard(),
            ]
            * 5
        )
        shuffle(self)


class DiscardPile(CardPile):
    def __init__(self):
        super().__init__()


# 游戏类
# 游戏的回合分为已经进行的回合，正在进行的回合，将要生成的回合
# 回合和轮次不同
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
# 这个回合是角色的一个完整回合
class Turn:
    def __init__(self, game: Game):
        for player in game.player_list:
            if player.have_draw_card_stage:
                yield DrawStage(player)
            if player.have_use_card_stage:
                yield UseStage(player)
            yield DiscardStage(player)


# 轮次类，里面包含多个回合
class Round:
    def __init__(self) -> None:
        pass
