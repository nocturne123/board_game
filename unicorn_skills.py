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
        """弃置一张牌，给目标挂接一个特效，当目标回血时受到伤害"""
        self.player.card_action.discard_card(card, discard_pile)
        if hasattr(target.data, "sunburst_mark"):
            target.data.sunburst_mark += 1
        else:
            pass

    def sunburst_mark(self):
        pass
