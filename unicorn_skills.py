from skill import CharacterSkill
from ENUMS.common_enums import DamageTypeEnum
from damage import Damage


class Sunburst_1(CharacterSkill):
    def __init__(self, player):
        super().__init__(player=player)
        self.name = "Not named yet"
        self.affected_list = []

    def register(self):
        self.registed = True

    def unregister(self):
        self.registed = False

    def use(self, card, target, discard_pile):
        """弃置一张牌，给目标挂接一个标记和一个回血时根据标记扣血的特效
        特效挂接到Hook_After_Healing上"""
        self.player.card_action.discard_card(card, discard_pile)
        # 打上标记，目标有标记则标记加1，同时将目标记录到affected_list中，技能失效时注销
        if hasattr(target.data, "sunburst_mark"):
            target.data.sunburst_mark += 1
        else:
            setattr(target.data, "sunburst_mark", 1)
        if self.sunburst_hurt_after_healing not in target.data.Hook_After_Healing:
            target.data.Hook_After_Healing.append(self.sunburst_hurt_after_healing)
        self.affected_list.append(target)

    def sunburst_hurt_after_healing(self):
        pass
