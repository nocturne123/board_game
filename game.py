import abc

from player import Player
from collections import deque
from ENUMS import GameModeEnum, CharaterAliveEnum
from team import Team
from random import shuffle
from itertools import chain, zip_longest
from collections import deque
from player_action import PlayerAction


# 游戏类
# 游戏的回合分为已经进行的回合，正在进行的回合，将要生成的回合
# 回合和轮次不同
class Game:
    def __init__(self):
        self.player_list = None
        self.draw_pile = None
        self.map = None
        self.game_mode = None
        self.team_deque: deque[Team] = deque()
        # 最开始的玩家
        self.current_player = None

    def add_player(self, *players: Player):
        self.player_list = [*players]
        shuffle(self.player_list)

    def game_set_gamemode(self, gamemode):
        self.game_mode = gamemode

    def game_set_map(self, map):
        self.map = map

    def game_set_pile(self, drawpile, discardpile):
        self.draw_pile = drawpile
        self.discard_pile = discardpile

    # 队伍基础分配
    def set_team(self):
        if self.game_mode == GameModeEnum.FFA:
            for player in self.player_list:
                solo_team = Team(maxlen=1)
                solo_team.append(player)
                self.team_deque.append(solo_team)

        elif self.game_mode == GameModeEnum.two_vs_two:
            team1_member = self.player_list[0:2]
            team2_member = self.player_list[2:4]
            team1 = Team(maxlen=2)
            team2 = Team(maxlen=2)
            team1.extend(team1_member)
            team2.extend(team2_member)
            self.team_deque.extend([team1, team2])

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
            self.team_deque.extend([team1, team2, team3])

        elif self.game_mode == GameModeEnum.three_vs_three:
            team1_member = self.player_list[0:3]
            team2_member = self.player_list[3:6]
            team1 = Team(maxlen=3)
            team2 = Team(maxlen=3)
            team1.extend(team1_member)
            team2.extend(team2_member)
            self.team_deque.extend([team1, team2])

    @property
    def alive_team_deque(self):
        return deque(team for team in self.team_deque if team.is_remaining)

    def next_alive_team(self):
        a = self.team_deque.popleft()
        self.team_deque.append(a)
        if self.is_remaining:
            while self[0].living_stage == CharaterAliveEnum.dead:
                a = self.popleft()
                self.append(a)
        else:
            pass

    def game_start_dealing(self):
        for player in self.player_list:
            for i in range(player.start_game_draw):
                card = self.draw_pile.pop()
                card.get_draw()
                player.hand_sequence.append(card)
                card.get_into_hand()

    def set_round_list(self):
        """返回当前玩家的优先级序列，可以视作玩家观察到的轮次"""
        return [
            player
            for player in chain.from_iterable(zip_longest(*self.team_deque))
            if player.living_stage != CharaterAliveEnum.dead
        ]

    def set_player_to_current(self):
        self.current_player = self.team_deque[0][0]

    def set_current_player_start_turn(self):
        self.current_player.start_turn()  # 开始回合，进入准备阶段
        self.current_player.end_prepare()  # 结束准备阶段，进入抽牌阶段
        PlayerAction.draw_card_from_pile(
            self.current_player,
            self.draw_pile,
            self.current_player.draw_stage_card_number,
        )  # 玩家抽牌

        self.current_player.end_draw()  # 玩家结束抽牌阶段，进入出牌阶段


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
