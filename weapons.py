from card import Card, transtions
from ENUMS.common_enums import CardTypeEnum, CardStateEnum
from ENUMS.weapon_card_enums import WeaponIdentity
from abc import abstractmethod


# TODO:武器的攻击距离逻辑需要设计，现在的乐器的实现是不带攻击距离的
class BaseWeapon(Card):
    def __init__(
        self,
        attack_distence,
        states=CardStateEnum,
        transitions=transtions,
    ):
        super().__init__(
            card_type=CardTypeEnum.weapon, states=states, transitions=transitions
        )
        self.attack_distence = attack_distence

    @abstractmethod
    def register(self, user):
        """注册时的效果，也就是生效，卡牌在装备时调用这个函数，进行'生效'。"""
        pass

    @abstractmethod
    def unregister(self, user):
        """注销时的效果，当装备失效时，装备不会从装备栏中消失，而是调用这个函数，进行'失效'。"""
        pass

    def equiped(self, user):
        """装备时的效果"""
        self.register(user)

    def unequiped(self, user):
        """卸下时的效果"""
        self.unregister(user)

    @abstractmethod
    def effect(self, user, target):
        """卡牌产生效果"""
        self.equiped(user)

    def __repr__(self):
        return f"{self.identity}: {self.description}"


class Instrument(BaseWeapon):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(attack_distence=2, states=states, transitions=transitions)
        self.identity = WeaponIdentity.instrument
        self.description = "Heal 1 when dealing damage more than 1"

    def heal_1_after_dealing_damage(self, player_action, damage_int):
        if damage_int > 1:
            player_action.heal(1)

    def register(self, user):
        if self.heal_1_after_dealing_damage not in user.data.Hook_After_Dealing_Damage:
            user.data.Hook_After_Dealing_Damage.append(self.heal_1_after_dealing_damage)

    def unregister(self, user):
        if self.heal_1_after_dealing_damage in user.data.Hook_After_Dealing_Damage:
            user.data.Hook_After_Dealing_Damage.remove(self.heal_1_after_dealing_damage)


class Machine(BaseWeapon):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(attack_distence=1, states=states, transitions=transitions)
        self.identity = WeaponIdentity.machine
        self.description = "Draw 1 more card at drawing stage"

    def register(self, user):
        user.data.draw_stage_card_number += 1

    def unregister(self, user):
        user.data.draw_stage_card_number -= 1


class Bouquet(BaseWeapon):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(attack_distence=1, states=states, transitions=transitions)
        self.identity = WeaponIdentity.bouquet
        self.description = "You can discard a card and draw a card,twice per turn"

    def discard_a_card_and_draw_a_card(self, player, card, drawpile, discard_pile):
        self.use_twice_in_turn()
        player.card_action.discard_card(card, discard_pile)
        player.card_action.draw_card(drawpile, 1)
