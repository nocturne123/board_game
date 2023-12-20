import abc

from player import Player
from collections import deque
from ENUMS.common_enums import CharaterAliveEnum, GameModeEnum
from team import Team
from random import shuffle
from itertools import chain, zip_longest
from collections import deque
from player_data import PlayerData
from card_action import CardAction


# 游戏类
# 回合和轮次不同
# 游戏类主持开一局游戏的逻辑，组织玩家，组织抽牌堆、弃牌堆，组织地图，判断胜负。
# 其中，最重要的就是胜负关系的判断，判断完胜负后游戏结束。
# 游戏类负责指挥一个玩家的回合结束后，下一个玩家的回合开始
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
        """添加玩家"""
        self.player_list = [*players]
        shuffle(self.player_list)

    def game_set_gamemode(self, gamemode):
        """设置游戏模式"""
        self.game_mode = gamemode

    def game_set_map(self, map):
        """设置地图"""
        self.map = map

    def game_set_pile(self, drawpile, discardpile):
        """设置牌堆，包括抽牌堆和弃牌堆"""
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

    def next_team(self):
        # 这个地方变相写了一个do-while循环，先把第二位的Team排上来，检测这个Team还活着没有
        # 没有的话，就再把下一个第二位的Team排上来
        while True:
            a = self.team_deque.popleft()
            self.team_deque.append(a)
            if self.team_deque[0].is_remaining:
                break

    def game_start_dealing(self):
        for player in self.player_list:
            player.card_action.draw_card(self.draw_pile, player.data.start_game_draw)

    def set_round_list(self):
        """返回当前玩家的优先级序列，可以视作玩家观察到的轮次"""
        return [
            player
            for player in chain.from_iterable(zip_longest(*self.team_deque))
            if player.living_stage != CharaterAliveEnum.dead
        ]

    def set_player_to_current(self):
        self.current_player: Player = self.team_deque[0][0]

    def set_current_player_start_turn(self):
        self.current_player.player_action.start_turn()  # 开始回合，进入准备阶段
        self.current_player.player_action.start_turn_init()  # 玩家回合开始时的初始化
        self.current_player.player_action.start_draw()  # 结束准备阶段，进入抽牌阶段
        self.current_player.card_action.draw_card(
            self.draw_pile,
            self.current_player.data.draw_stage_card_number,
        )  # 玩家抽牌

        self.current_player.player_action.start_play()  # 玩家结束抽牌阶段，进入出牌阶段

    # TODO：优化逻辑
    def winning_team(self):
        """根据team_deque中的队伍，判断胜负，只剩一只队伍时，剩下的那只队伍获得胜利"""
        return len(self.alive_team_deque) > 1


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
