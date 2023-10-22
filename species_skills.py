"""种族技能的实现，飞马的技能暂时不写，因为地面效果还没写"""
from skill import SpeciesSkill
from player import Player


class UnicornSkill(SpeciesSkill):
    """独角兽技能 ,攻击距离+1"""

    def __init__(self):
        super().__init__()

    def register(self, user: Player):
        user.data.attack_distance += 1

    def unregister(self, user: Player):
        user.data.attack_distance -= 1

    def use(self, user: Player, target):
        pass


class EarthponySkill(SpeciesSkill):
    """地种技能 ,攻击时投一个色子，大于3则造成额外1点伤害"""

    def __init__(self):
        super().__init__()

    def register(self, user: Player):
        pass

    def unregister(self, user: Player):
        pass

    def use(self, user: Player, target):
        pass
