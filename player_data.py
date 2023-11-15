from charaters import Charater

from ENUMS.common_enums import (
    PlayerStateEnum,
    CharaterAliveEnum,
    SpeciesEnum,
    DamageTypeEnum,
    CharaterAliveEnum,
)
from damage import Damage

from transitions import Machine

stage_transitions = [
    {
        "trigger": "start_turn",
        "source": PlayerStateEnum.wait,
        "dest": PlayerStateEnum.prepare,
    },
    {
        "trigger": "start_draw",
        "source": PlayerStateEnum.prepare,
        "dest": PlayerStateEnum.draw,
    },
    {
        "trigger": "start_play",
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
    {
        "trigger": "end_turn",  # 用于结束回合
        "source": PlayerStateEnum.end,
        "dest": PlayerStateEnum.wait,
    },
    {
        "trigger": "skip_turn",  # 用于跳过回合
        "source": PlayerStateEnum.prepare,
        "dest": PlayerStateEnum.end,
    },
    {
        "trigger": "skip_draw",  # 用于跳过抽牌阶段
        "source": PlayerStateEnum.prepare,
        "dest": PlayerStateEnum.play,
    },
    {
        "trigger": "skip_play",  # 用于跳过出牌阶段
        "source": PlayerStateEnum.draw,
        "dest": PlayerStateEnum.discard,
    },
    {
        "trigger": "skip_discard",  # 用于跳过弃牌阶段
        "source": PlayerStateEnum.play,
        "dest": PlayerStateEnum.end,
    },
]

living_stage_transitions = [
    {
        "trigger": "die",
        "source": CharaterAliveEnum.alive,
        "dest": CharaterAliveEnum.dead,
    },
    {
        "trigger": "faint",
        "source": CharaterAliveEnum.alive,
        "dest": CharaterAliveEnum.fainted,
    },
    {
        "trigger": "awake",
        "source": CharaterAliveEnum.fainted,
        "dest": CharaterAliveEnum.alive,
    },
]


class PlayerData:
    def __init__(self, cha: Charater):
        """玩家类实现，玩家不涉及具体卡牌的hook统一挂接在player.data里面"""
        self.health = cha.health
        self.speed = cha.speed
        self.name = cha.name
        self.species = cha.species

        # 技能栏，分为种族技能、角色技能、装备技能
        self.species_skills = []
        self.character_skills = []
        self.equipment_skills = []

        # 玩家的装备栏
        self.equipment_sequence = []

        # 玩家的武器槽、防具槽、元素槽，装备之后变为True
        self.weapon_slot = False
        self.armor_slot = False
        self.element_slot = False

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

        # 角色的攻击距离
        self.attack_distance = 0

        # 角色的三种基本防御
        self.physical_defense = 0
        self.magic_defense = 0
        self.mental_defense = 0

        # 角色的基础生命值和最大生命值
        self.base_health = cha.health
        self.max_health = cha.health

        # 角色在回合开始时的抽牌数量
        self.draw_stage_card_number = 2

        # 角色初始手牌数量
        self.start_game_draw = 4

        # 角色最大手牌数量
        self.max_hand_sequence_num = 6

        # 玩家移动次数和攻击次数，在回合开始时，用这个属性来初始化
        self.move_chance = 1
        self.attack_chance = 1

        # 玩家在回合种的移动和攻击次数，用于记录玩家在回合中的移动和攻击次数
        self.move_chance_in_turn = 0
        self.attack_chance_in_turn = 0

        """以下属性为状态机相关属性"""
        # 玩家阶段状态，先为空，在后面利用函数补充
        self.stage_state = None

        # 玩家生存状态，先为空，同上
        self.living_state = None

        # 玩家上一轮的生命值，初始时为最大生命值，在回合结束时记录，给沙漏使用
        self.health_last_turn = self.max_health

        # 玩家的回合计数
        self.turn_count = 0

        # 玩家的轮次计数
        self.round_count = 0

        # 玩家是否被沉默，分为装备栏沉默，种族技能沉默，技能沉默
        self.muted_equipment = False
        self.muted_species_skill = False
        self.muted_skill = False

        # 玩家被沉默之后，取消注册的技能被挂起，挂在对应的列表里面
        self.hold_equipment = []
        self.hold_species_skill = []
        self.hold_skill = []

        # 玩家在治疗前后的hook
        self.Hook_Before_Healing = []
        self.Hook_After_Healing = []

        # 使用卡牌前后的hook
        self.Hook_Before_Use = []
        self.Hook_After_Use = []

        # 玩家在被指定后的hook
        # 这个hook在card的use阶段调用
        # 小呆的技能挂在这里
        self.Hook_After_Chosen = []

        # 卡牌生效前的hook，
        # 在使用卡牌后、卡牌生效前也就是effect前调用，
        # 无畏天马的技能挂在这里
        self.Hook_Before_Effect = []

        # 卡牌生效后的hook
        # 在卡牌生效后也就是effect后调用
        self.Hook_After_Effect = []

        # 玩家在被卡牌指定后，生效前的hook
        # 作为被动技能，类似于受到卡牌效果后触发的技能
        self.Hook_Before_Effect_As_Target = []

        # 玩家在被卡牌指定后，生效后的hook
        self.Hook_After_Effect_As_Target = []

        # 玩家在受到伤害前后的hook
        self.Hook_After_Receive_Damage = []
        self.Hook_Before_Receive_Damage = []

    def stage_state_init(self, transitions=stage_transitions):
        """玩家阶段状态，用于表示玩家当前处于哪个阶段,阶段包括等待阶段、
        准备阶段、抽牌阶段、出牌阶段、弃牌阶段、结束阶段"""
        # 基础状态机，初始化为等待状态
        self.stage_state = Machine(
            states=PlayerStateEnum,
            transitions=transitions,
            initial=PlayerStateEnum.wait,
        )

    def living_state_init(self, transitions=living_stage_transitions):
        """玩家生存状态，用于表示玩家当前处于哪个状态，状态包括存活、昏迷、死亡"""
        self.living_state = Machine(
            states=CharaterAliveEnum,
            transitions=transitions,
            initial=CharaterAliveEnum.alive,
        )
