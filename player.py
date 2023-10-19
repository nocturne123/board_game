"""这个文件是玩家操作的文件，现阶段全部用静态方法实现。
未来需要用类进行包装。实现hook机制，实现玩家操作的可扩展性，方便技能的实现。
注：卡牌的状态切换先于卡牌的相关操作，先切换，再操作"""
"""2023.10.18：将使用卡牌的逻辑剔除出PlayerAction，PlayerAction中的操作只涉及Player类的
数值操作、状态改变等，例如血量的增加减少、抽牌数的增加减少、受到伤害，以及回合相关操作，比如
结束回合、跳过回合。"""
from player_data import PlayerData
from damage import Damage

from ENUMS.common_enums import (
    PlayerStateEnum,
    CharaterAliveEnum,
    SpeciesEnum,
    DamageTypeEnum,
    CardTypeEnum,
    CardStateEnum,
)

from player_exceptions import (
    NotInPlayStateException,
    NoChanceToAttackException,
    ImmuneToAttackException,
    ImmuneToStealException,
)


class Player:
    """玩家操作类"""

    def __init__(self, player_data) -> None:
        self.data: PlayerData = player_data
        self.Hook_Bofore_Healing = []
        self.Hook_After_Healing = []

    def living_update(self):
        # TODO:有关收藏品的逻辑没有更新
        if self.data.health <= 0:
            self.data.living_state.die()

    def decrease_health(self, num: int):
        """玩家减少生命值"""
        self.data.health -= num
        self.living_update(self)

    def receive_damage(self, damage: Damage):
        """玩家受到伤害"""
        if damage.type == DamageTypeEnum.physical:
            received_damage = damage.num - self.data.physical_defense
        elif damage.type == DamageTypeEnum.magic:
            received_damage = damage.num - self.data.magic_defense
        elif damage.type == DamageTypeEnum.mental:
            received_damage = damage.num - self.data.mental_defense
        self.decrease_health(self, received_damage)
        return received_damage

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
        self.data.move_chance_in_turn = self.data.move_chance
        self.data.attack_chance_in_turn = self.data.attack_chance

    def heal(self, num: int):
        """玩家回复生命值"""
        if self.Hook_Bofore_Healing != []:
            for func in self.Hook_Bofore_Healing:
                func(self.data, num)
        self.data.health += num
        self.living_update(self)
        if self.Hook_After_Healing != []:
            for func in self.Hook_After_Healing:
                func(self.data, num)
