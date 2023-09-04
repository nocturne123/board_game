from game import Game
from charaters import Charater

from ENUMS import PlayerStateEnum, CharaterAliveEnum, SpeciesEnum

from transitions import Machine


class Player:
    def __init__(self, cha: Charater, game: Game):
        """以下属性直接来自于player.py文件"""
        self.health = cha.health
        self.speed = cha.speed
        self.skills = []
        self.name = cha.name
        self.species = cha.species
        self.game = game

        # 玩家的武器、护甲均为空列表形式，因为红龙能装多个装备，设计为列表也方便未来的扩展
        self.armor = []
        self.weapon = []

        # 玩家手牌
        self.hand_sequence = []

        # 玩家收集品
        self.colloctions = []

        # 玩家可否被选中，主要针对特殊状态，例如晕眩、针线提供的无敌、余晖烁烁的无敌、王冠提供的无敌
        # 根据技能描述，线轴为不会受到伤害，余晖烁烁、王冠为不能成为攻击牌目标，增加不可被攻击选中的属性
        # 攻击不可被选中在攻击牌类种实现，玩家类仅提供属性
        # 玩家可否被偷窃，也写在这里
        self.is_selectable = True
        self.immune_from_attack = False
        self.immune_from_steal = False

        # 玩家id，未来看是否会用到
        self.id = 0

        # 角色的三种基本攻击
        self.physical_attack = cha.physical_attack
        self.magic_attack = cha.magic_attack
        self.mental_attack = cha.mental_attack

        # 角色的基础生命值和最大生命值
        self.base_health = cha.health
        self.max_health = cha.health

        # 角色在回合开始时的抽牌数量
        self.draw_stage_card_number = 2

        # 角色初始手牌数量
        self.start_game_draw = 4

        # 角色最大手牌数量
        self.max_hand_sequence = 6

        # 玩家移动次数和攻击次数
        self.move_chance = 1
        self.attack_chance = 1

        """以下属性为状态机相关属性"""
        # 玩家阶段状态，先为空，在后面利用函数补充
        self.stage_state = None

        # 玩家生存状态，先为空，同上
        self.living_state = None

    def stage_state_init(self):
        """玩家阶段状态，用于表示玩家当前处于哪个阶段,阶段包括等待阶段、
        准备阶段、抽牌阶段、出牌阶段、弃牌阶段、结束阶段"""
        # 基础状态机，初始化为等待状态
        self.stage_state = Machine(states=PlayerStateEnum, initial=PlayerStateEnum.wait)
        transitions = [
            {
                "trigger": "end_prepare",
                "source": PlayerStateEnum.prepare,
                "dest": PlayerStateEnum.draw,
            },
            {
                "trigger": "end_draw",
                "source": PlayerStateEnum.draw,
                "dest": PlayerStateEnum.play,
            },
            {
                "trigger": "end_play",
                "source": PlayerStateEnum.play,
                "dest": PlayerStateEnum.discard,
            },
            {
                "trigger": "end_discard",
                "source": PlayerStateEnum.discard,
                "dest": PlayerStateEnum.end,
            },
        ]
