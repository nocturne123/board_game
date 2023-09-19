from random import shuffle
import abc

# from player import Player
from collections import deque
from ENUMS import GameModeEnum, CharaterAliveEnum
from team import Team
from random import shuffle
from itertools import chain, zip_longest

from card_pile import DrawPile, DiscardPile


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
    # turn类被取消了
    def start_stage(self, drawpile, player: Player):
        player.draw_card(drawpile, num=player.draw_stage_card_number)

    def end_stage(self, player):
        player.end_stage(self)


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


# 游戏类
# 游戏的回合分为已经进行的回合，正在进行的回合，将要生成的回合
# 回合和轮次不同
class Game:
    def __init__(self, gamemode, map, draw_pile, *players):
        self.player_list = shuffle([*players])
        self.draw_pile = draw_pile
        self.map = map
        self.game_mode = gamemode
        self.team_list = []
        # 最开始的玩家
        self.current_player = self.team_list[0][0]

    # 队伍基础分配
    def set_team(self):
        if self.game_mode == GameModeEnum.FFA:
            for player in self.player_list:
                solo_team = Team(maxlen=1)
                solo_team.append(player)
                self.team_list.append(solo_team)

        elif self.game_mode == GameModeEnum.two_vs_two:
            team1_member = self.player_list[0:2]
            team2_member = self.player_list[2:4]
            team1 = Team(maxlen=2)
            team2 = Team(maxlen=2)
            team1.extend(team1_member)
            team2.extend(team2_member)
            self.team_list.extend([team1, team2])

        elif self.game_mode == GameModeEnum.FFA_two:
            team1_member = self.player_list[0:2]
            team2_member = self.player_list[2:4]
            team3_member = self.player_list[4:6]
            team1 = Team(maxlen=2)
            team2 = Team(maxlen=2)
            team3 = Team(maxlen=2)
            team1.extend(team1_member)
            team2.extend(team2_member)
            team3.extend(team3_member)
            self.team_list.extend([team1, team2, team3])

        elif self.game_mode == GameModeEnum.three_vs_three:
            team1_member = self.player_list[0:3]
            team2_member = self.player_list[3:6]
            team1 = Team(maxlen=3)
            team2 = Team(maxlen=3)
            team1.extend(team1_member)
            team2.extend(team2_member)
            self.team_list.extend([team1, team2])

    def start_stage(self, stage, player):
        pass

    def end_stage(self, stage, player):
        pass

    def start_turn(self, player):
        pass

    def game_start_dealing(self):
        for player in self.player_list:
            player.first_round_draw(self.draw_pile)

    # 返回当前玩家的优先级序列，可以视作玩家观察到的轮次
    def set_round_list(self):
        return [
            player
            for player in chain.from_iterable(zip_longest(*self.team_list))
            if player.living_status != CharaterAliveEnum.dead
        ]


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


# 轮次类，里面包含多个回合，游戏逻辑更新后，以角色看到的优先级序列作为轮次的实现
# 优先级序列由game类计算并提供，round类内部只做保存
# 轮次类储存上轮伤害来源、弃牌造成伤害的信息
class Round(list):
    def __init__(self, game):
        super().__init__
        # 只储存还能进行游戏的玩家
        self.player_list = [
            player
            for player in game.player_list
            if player.living_status != CharaterAliveEnum.dead
        ]

    def round_update(self):
        while tuple(self) != tuple(self.player_list):
            pass
