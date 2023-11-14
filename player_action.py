"""这个文件是玩家操作的文件，现阶段全部用静态方法实现。
未来需要用类进行包装。实现hook机制，实现玩家操作的可扩展性，方便技能的实现。
注：卡牌的状态切换先于卡牌的相关操作，先切换，再操作"""
"""2023.10.18：将使用卡牌的逻辑剔除出PlayerAction，PlayerAction中的操作只涉及Player类的
数值操作、状态改变等，例如血量的增加减少、抽牌数的增加减少、受到伤害，以及回合相关操作，比如
结束回合、跳过回合。"""
from player_data import PlayerData
from damage import Damage
import random
from ENUMS.common_enums import (
    PlayerStateEnum,
    CharaterAliveEnum,
    SpeciesEnum,
    DamageTypeEnum,
    CardTypeEnum,
    CardStateEnum,
)


class PlayerAction:
    """玩家操作类"""

    def __init__(self, player_data) -> None:
        self.data: PlayerData = player_data
        # 玩家数据的状态机初始化在这一步完成，这样当玩家数据初始化时，状态机也会初始化
        self.data.stage_state_init()
        self.data.living_state_init()

    def living_update(self):
        # TODO:有关收藏品的逻辑没有更新
        if self.data.health <= 0:
            self.data.living_state.die()

    def decrease_health(self, num: int):
        """玩家减少生命值"""
        self.data.health -= num
        self.living_update()

    def receive_damage(self, damage: Damage):
        """玩家受到伤害"""
        if self.data.Hook_Before_Receiving_Damage:
            for func in self.data.Hook_Before_Receiving_Damage:
                func(self, damage)
        if damage.type == DamageTypeEnum.physical:
            received_damage = damage.num - self.data.physical_defense
        elif damage.type == DamageTypeEnum.magic:
            received_damage = damage.num - self.data.magic_defense
        elif damage.type == DamageTypeEnum.mental:
            received_damage = damage.num - self.data.mental_defense
        elif damage.type == DamageTypeEnum.real:
            received_damage = damage.num
        self.decrease_health(received_damage)
        if self.data.Hook_After_Receiving_Damage:
            for func in self.data.Hook_After_Receiving_Damage:
                func(self, damage)
        return received_damage

    def start_turn(self):
        """开始回合"""
        self.data.stage_state.start_turn()  # 玩家状态切换，从wait切换到prepare

    def start_draw(self):
        """结束准备阶段,抽牌阶段开始"""
        self.data.stage_state.start_draw()  # 玩家状态切换，从prepare切换到draw

    def start_play(self):
        """结束抽牌阶段，出牌阶段开始"""
        self.data.stage_state.start_play()

    def end_play(self):
        """结束回合"""
        if len(self.data.hand_sequence) <= self.data.max_hand_sequence_num:
            self.data.stage_state.skip_discard()
            self.data.stage_state.end_turn()
        else:
            self.data.stage_state.end_play()

    def end_discard(self):
        """结束阶段"""
        self.data.stage_state.end_discard()

    def end_turn(self):
        """结束回合"""
        self.data.stage_state.end_turn()

    def start_turn_init(self):
        """回合开始时的初始化"""
        # 当到自己回合时无论如何回合计数都会加1，轮次计数因为玩家不能从game类里获取信息，所以轮次计数在game类里实现
        self.data.turn_count += 1

        # 回合开始时，玩家的移动次数和攻击次数都会重置
        self.data.move_chance_in_turn = self.data.move_chance
        self.data.attack_chance_in_turn = self.data.attack_chance

    def heal(self, num: int):
        """玩家回复生命值"""
        if self.data.Hook_Before_Healing != []:
            for func in self.data.Hook_Bofore_Healing:
                func(self, num)
        self.data.health += num
        if self.data.health > self.data.max_health:
            self.data.health = self.data.max_health
        self.living_update()
        if self.data.Hook_After_Healing != []:
            for func in self.data.Hook_After_Healing:
                func(self, num)

    def roll_dice(self):
        """玩家掷色子"""
        num = random.randint(1, 6)
        return num

    def roll_earthpony_dice(self):
        """陆马技能的色子和普通色子分开"""
        num = random.randint(1, 6)
        return num
