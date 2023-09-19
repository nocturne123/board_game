from ENUMS import CardTypeEnum
import abc


# 牌类简易实现，现阶段只实现了牌的类型分类
# 卡牌在抽取、弃置、打出时都会产生效果
# 具体的实现为：get_xxx、on_xxx、xxx
# get为被调用、on为打出、弃掉那一刻发生的事情、可被技能响应
# 例如被抽起来、被打出、被弃掉
#
# 2023.9.4设计更新，全面采用状态机


class Card(metaclass=abc.ABCMeta):
    def __init__(self, draw_pile, discard_pile):
        self.distance_limited = True
        self.draw_pile = draw_pile
        self.discard_pile = discard_pile

    @abc.abstractclassmethod
    def card_type(self) -> CardTypeEnum:
        return CardTypeEnum

    # 所有卡牌的核心机制
    @abc.abstractclassmethod
    def take_effect(self, target):
        pass

    # 卡牌被使用时调用的函数，此时卡牌在玩家手里，马上打出
    def get_used(self, card_user, target):
        self.on_use(card_user, target)

    # 卡牌被打出，进入结算阶段,此时卡牌进入弃牌堆
    def on_use(self, card_user, target):
        self.take_effect(card_user, target)

    # 卡牌在被抽起时发生的事情
    def on_draw(self, card_user):
        pass

    # 卡牌被弃置，对应get_used()
    def get_discard(self, card_user):
        self.on_discard(card_user)

    # 卡牌在被弃置时发生的事情

    def on_discard(self, card_user):
        self.get_into_discard_pile(card_user)

    # 卡牌进入弃牌堆时发生的事情，角色收集品被弃置时，会抽取奖励牌，由此方法实现
    def get_into_discard_pile(self, card_user):
        self.discard_pile.append(self)


# 物理攻击卡牌类
class PhysicalAttackCard(Card):
    def __init__(self):
        super().__init__()

    def card_type(self):
        return CardTypeEnum.physical_attack

    def on_use(self, card_user: Player, target):
        if card_user.attack_chance >= 1:
            self.take_effect(card_user, target)
            card_user.attack_chance -= 1
        else:
            print(f"{card_user.name}，你本回合内没有攻击次数了")

    def take_effect(self, card_user: Player, target):
        damage = card_user.attack[1]

        target.get_damage((damage, card_user))
        self.get_into_discard_pile(card_user)

    def __repr__(self) -> str:
        return "physical attack"


# 魔法攻击类卡牌
class MagicAttackCard(Card):
    def __init__(self):
        super().__init__()

    def card_type(self):
        return CardTypeEnum.magic_attack

    def on_use(self, card_user: Player, target):
        if card_user.attack_chance >= 1:
            self.take_effect(card_user, target)
            card_user.attack_chance -= 1
        else:
            print(f"{card_user.name}，你本回合内没有攻击次数了")

    def take_effect(self, card_user, target):
        damage = card_user.attack[0]
        target.get_damage((damage, card_user, self))
        self.get_into_discard_pile(card_user)

    def __repr__(self) -> str:
        return "magic attack"


# 心理攻击类卡牌
class MentalAttackCard(Card):
    def __init__(self):
        super().__init__()

    def card_type(self):
        return CardTypeEnum.mental_attack

    def on_use(self, card_user: Player, target):
        if card_user.attack_chance >= 1:
            self.take_effect(card_user, target)
            card_user.attack_chance -= 1
        else:
            print(f"{card_user.name}，你本回合内没有攻击次数了")

    def take_effect(self, card_user, target):
        damage = card_user.attack[2]
        target.get_damage((damage, card_user, self))
        self.get_into_discard_pile(card_user)

    def __repr__(self) -> str:
        return "mental attack"


class StealCard(Card):
    def __init__(self):
        super().__init__()

    def take_effect(self, card_user, target):
        pass

    def __repr__(self) -> str:
        return "Steal"
