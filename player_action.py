"""这个文件是玩家操作的文件，现阶段全部用静态方法实现。
未来需要用类进行包装。实现hook机制，实现玩家操作的可扩展性，方便技能的实现。
注：卡牌的状态切换先于卡牌的相关操作，先切换，再操作"""
"""2023.10.18：将使用卡牌的逻辑剔除出PlayerAction，PlayerAction中的操作只涉及Player类的
数值操作、状态改变等，例如血量的增加减少、抽牌数的增加减少、受到伤害，以及回合相关操作，比如
结束回合、跳过回合。"""
from player import Player
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
    NeedTargetException,
    NeedFurtherTargetException,
    ImmuneToAttackException,
    ImmuneToStealException,
)


class PlayerAction:
    """玩家操作类"""

    Hook_Bofore_Healing = []
    Hook_After_Healing = []

    def __init__(self, player) -> None:
        self.player: Player = player

    def living_update(self):
        # TODO:有关收藏品的逻辑没有更新
        if self.player.health <= 0:
            self.player.living_state.die()

    def decrease_health(self, num: int):
        """玩家减少生命值"""
        self.player.health -= num
        self.living_update(self)

    def receive_damage(self, damage: Damage):
        """玩家受到伤害"""
        if damage.type == DamageTypeEnum.physical:
            received_damage = damage.num - self.player.physical_defense
        elif damage.type == DamageTypeEnum.magic:
            received_damage = damage.num - self.player.magic_defense
        elif damage.type == DamageTypeEnum.mental:
            received_damage = damage.num - self.player.mental_defense
        self.decrease_health(self, received_damage)
        return received_damage

    def end_play(self):
        """结束回合"""
        if len(self.player.hand_sequence) <= self.player.max_hand_sequence_num:
            self.player.stage_state.skip_discard()
            self.player.stage_state.end_turn()
        else:
            self.player.stage_state.end_play()

    def end_discard(self):
        """结束阶段"""
        self.player.stage_state.end_discard()

    def end_turn(self):
        """结束回合"""
        self.player.stage_state.end_turn()

    def start_turn_init(self):
        """回合开始时的初始化"""
        self.player.move_chance_in_turn = self.player.move_chance
        self.player.attack_chance_in_turn = self.player.attack_chance

    def heal(self, num: int):
        """玩家回复生命值"""
        if PlayerAction.Hook_Bofore_Healing != []:
            for func in PlayerAction.Hook_Bofore_Healing:
                func(self.player, num)
        self.player.health += num
        self.living_update(self)
        if PlayerAction.Hook_After_Healing != []:
            for func in PlayerAction.Hook_After_Healing:
                func(self.player, num)
