"""种族技能的实现，飞马的技能暂时不写，因为地面效果还没写"""
from skill import SpeciesSkill
from ENUMS.common_enums import SpeciesEnum, CardTypeEnum
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
        self.sucessful_dice_num = 3

    @property
    def is_on(self):
        """判断技能是否开启，当自动生效且没有事件影响时，技能开启"""
        return self.auto_use and self.forced_switch

    # 技能挂到挂钩之前应判断是否挂过，防止重复挂钩
    def send_func_to_card(self, card):
        if self.damage_add_1 not in card.hook_change_effect:
            card.hook_change_effect.append(self.damage_add_1)
        else:
            pass

    # 将投骰子的判断添加到player.data的Hook_Before_Effect中
    def send_func_to_player(self):
        if self.dice_judge not in self.player.data.Hook_Before_Effect:
            self.player.data.Hook_Before_Effect.append(self.dice_judge)

    # 对应的，取消注册时，将投色子的判断函数从player.data的Hook_Before_Effect中移除
    def remove_func_from_player(self):
        if self.dice_judge in self.player.data.Hook_Before_Effect:
            self.player.data.Hook_Before_Effect.remove(self.dice_judge)

    # 进行一次陆马投色子判断，成功则将伤害加1挂接到卡牌上
    def dice_judge(self, card_action, card, target, discard_pile):
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            if (
                self.player.player_action.roll_earthpony_dice()
                > self.sucessful_dice_num
            ):
                self.send_func_to_card(card)

    # 技能注册前应判断是否有这个技能，防止重复注册
    def register(self):
        self.registed = True
        self.send_func_to_player()

    def unregister(self):
        self.registed = False
        self.remove_func_from_player()

    @staticmethod
    def damage_add_1(damage: Damage):
        damage.num += 1


class OtherSkill(SpeciesSkill):
    """其他种族技能，初始摸牌数+3，昏厥后摸两张牌"""

    # TODO:现在没有实现昏厥相关，所以昏厥后摸两张牌未实现

    def __init__(self, player):
        super().__init__(player=player)

    def register(self):
        self.registed = True
        self.player.data.start_game_draw += 3

    def unregister(self):
        self.registed = False
        self.player.data.start_game_draw -= 3
