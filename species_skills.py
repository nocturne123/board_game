"""种族技能的实现，飞马的技能暂时不写，因为地面效果还没写"""
from skill import SpeciesSkill
from player import Player
from damage import Damage


class UnicornSkill(SpeciesSkill):
    """独角兽技能 ,攻击距离+1"""

    def __init__(self, player):
        super().__init__(player=player)

    def register(self):
        self.registed = True
        self.player.data.attack_distance += 1

    def unregister(self):
        self.registed = False
        self.player.data.attack_distance -= 1


class EarthponySkill(SpeciesSkill):
    """地种技能 ,攻击时投一个色子，大于3则造成额外1点伤害"""

    def __init__(self, player):
        super().__init__(player=player)
        self.auto_use = True
        self.forced_switch = True

    @property
    def is_on(self):
        """判断技能是否开启，当自动生效且没有事件影响时，技能开启"""
        return self.auto_use and self.forced_switch

    # 技能挂到挂钩之前应判断是否挂过，防止重复挂钩
    def send_func_to_card(self, user_data, card, target, discard_pile):
        if self.damage_add_1 not in card.hook_change_effect:
            card.hook_change_effect.append(self.damage_add_1)
        else:
            pass

    # 技能注册前应判断是否有这个技能，防止重复注册
    def register(self):
        self.registed = True
        if self not in self.player.data.species_skills:
            self.player.data.species_skills.append(self)
        else:
            pass

    def unregister(self):
        self.registed = False
        if self in self.player.data.species_skills:
            self.player.data.species_skills.remove(self)

    def use(self, user: Player, target):
        pass

    @staticmethod
    def damage_add_1(damage: Damage):
        damage.num += 1


class OtherSkill(SpeciesSkill):
    """其他种族技能，初始摸牌数+3，昏厥后摸两张牌"""

    def __init__(self, player):
        super().__init__(player=player)

    def register(self):
        self.registed = True
        self.player.data.start_game_draw += 3

    def unregister(self):
        self.registed = False
        self.player.data.start_game_draw -= 3
