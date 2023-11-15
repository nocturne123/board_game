from skill import CharacterSkill, Skill
from ENUMS.common_enums import DamageTypeEnum
from damage import Damage


class Sunburst_1(CharacterSkill):
    """日光耀耀1技能，弃一张牌给目标Player上一个标记，目标如果有标记则标记数量+1，
    目标回血时触发标记，受到等同于标记数量的伤害"""

    def __init__(self, player):
        super().__init__(player=player)
        self.name = "Not named yet"
        self.affected_list = []

    def register(self):
        self.registed = True

    def unregister(self):
        """技能注销时清空所有标记，把所有目标的Hook_After_Healing中的特效清理掉"""
        self.registed = False
        for target in self.affected_list:
            if hasattr(target.data, "sunburst_mark"):
                delattr(target.data, "sunburst_mark")
            if self.sunburst_hurt_after_healing in target.data.Hook_After_Healing:
                target.data.Hook_After_Healing.remove(self.sunburst_hurt_after_healing)

    def use_once_in_turn(func):
        return super().use_once_in_turn(func=func)

    @Skill.use_once_in_turn
    def use(self, card, target, discard_pile):
        """弃置一张牌，给目标挂接一个标记和一个回血时根据标记扣血的特效
        特效挂接到Hook_After_Healing上"""
        if self.registed == True:
            self.player.card_action.discard_card(card, discard_pile)
            # 打上标记，目标有标记则标记加1，同时将目标记录到affected_list中，技能失效时注销
            if hasattr(target.data, "sunburst_mark"):
                target.data.sunburst_mark += 1
            else:
                setattr(target.data, "sunburst_mark", 1)
            if self.sunburst_hurt_after_healing not in target.data.Hook_After_Healing:
                target.data.Hook_After_Healing.append(self.sunburst_hurt_after_healing)
            self.affected_list.append(target)
        else:
            raise Exception("技能未注册，无法使用")

    def sunburst_hurt_after_healing(self, player_action, healing_num):
        """如果回血时有标记，按标记数量扣血"""
        if player_action.data.sunburst_mark:
            player_action.receive_damage(
                Damage(type=DamageTypeEnum.real, num=player_action.data.sunburst_mark)
            )
            player_action.data.sunburst_mark = 0
