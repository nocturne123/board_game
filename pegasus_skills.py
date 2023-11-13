from skill import CharacterSkill
from ENUMS.common_enums import DamageTypeEnum
from damage import Damage


class derpy_1(CharacterSkill):
    """小呆的1技能，在受到攻击牌指定时，攻击者受到1点真实伤害，
    自身打出攻击牌后受到1点真实伤害"""

    def __init__(self, player):
        super().__init__(player=player)

    def register(self):
        """将反伤和自伤分别挂接到Hook_After_Chosn和Hook_Before_Effect上"""
        self.registed = True
        if self.reflect_damage not in self.player.data.Hook_After_Chosen:
            self.player.data.Hook_After_Chosen.append(self.reflect_damage)
        if self.hurt_yourself not in self.player.data.Hook_Before_Effect:
            self.player.data.Hook_Before_Effect.append(self.hurt_yourself)

    def unregister(self):
        """把反伤和自伤从Hook_After_Chosn和Hook_Before_Effect上移除"""
        self.registed = False
        if self.reflect_damage in self.player.data.Hook_After_Chosen:
            self.player.data.Hook_After_Chosen.remove(self.reflect_damage)
        if self.hurt_yourself in self.player.data.Hook_Before_Effect:
            self.player.data.Hook_Before_Effect.remove(self.hurt_yourself)

    def reflect_damage(self, card_action, card, target, discard_pile):
        """反伤，当受到攻击牌指定时，攻击者受到1点真实伤害"""
        damage = Damage(num=1, type=DamageTypeEnum.real)
        card_action.player_action.receive_damage(damage)

    def hurt_yourself(self, card_action, card, target, discard_pile):
        """自伤"""
        damage = Damage(num=1, type=DamageTypeEnum.real)
        card_action.player_action.receive_damage(damage)
