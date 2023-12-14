from card import Card, transtions
from ENUMS.common_enums import CardTypeEnum, CardStateEnum
from ENUMS.weapon_card_enums import WeaponIdentity
from abc import abstractmethod
from skill import EquipmentSkill


# TODO:武器的攻击距离逻辑需要设计，现在的乐器的实现是不带攻击距离的
class BaseWeapon(Card):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(
            card_type=CardTypeEnum.weapon, states=states, transitions=transitions
        )
        # skill列表里面装装备内部定义的类，在equip的时候实例化
        self.skill = []
        # skill实例化之后装进skill_instance里面，
        # 方便装备卸下时从player_data里面删除
        self.skill_instance = []
        self.attack_distence = 0

    # 装备的技能在装备时实例化，而不是游戏开始卡牌实例化的时候就实例化
    def equiped(self, user):
        """装备时的效果"""
        """与防具不同的点在于，装备有一个攻击距离的属性，在装备时直接加到player_data上
        这样不论装备被沉默与否，攻击距离始终是在的"""
        user.data.attack_distence += self.attack_distence
        for skill in self.skill:
            self.skill_instance.append(skill(user))

    # 同理，装备被卸下时应该主动回收技能的实例
    def unequiped(self, user):
        """卸下时的效果"""
        user.data.attack_distence -= self.attack_distence
        for skill_instance in self.skill_instance:
            skill_instance.unregister()
            if skill_instance in user.data.equipment_skills:
                user.data.equipment_skills.remove(skill_instance)
            self.skill_instance.remove(skill_instance)

    @abstractmethod
    def effect(self, user, target):
        """卡牌产生效果"""
        self.equiped(user)

    def __repr__(self):
        return f"{self.identity}: {self.description}"


class Instrument(BaseWeapon):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.attack_distence = 2
        self.identity = WeaponIdentity.instrument
        self.description = "Heal 1 when dealing damage more than 1"
        self.skill.append(Instrument.InstrumentSkill)

    class InstrumentSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "InstrumentSkill"
            self.description = "Physical Defense +1, Magic Defense +1"

        def heal_1_after_dealing_damage(self, player_action, damage_int):
            if damage_int > 1:
                player_action.heal(1)

        def register(self):
            if (
                self.heal_1_after_dealing_damage
                not in self.player.data.Hook_After_Dealing_Damage
            ):
                self.player.data.Hook_After_Dealing_Damage.append(
                    self.heal_1_after_dealing_damage
                )

        def unregister(self):
            if (
                self.heal_1_after_dealing_damage
                in self.player.data.Hook_After_Dealing_Damage
            ):
                self.player.data.Hook_After_Dealing_Damage.remove(
                    self.heal_1_after_dealing_damage
                )


class Machine(BaseWeapon):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.attack_distence = 1
        self.identity = WeaponIdentity.machine
        self.description = "Draw 1 more card at drawing stage"
        self.skill.append(Machine.MachineSkill)

    class MachineSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "MachineSkill"
            self.description = "Draw 1 more card at drawing stage"

        def register(self):
            self.player.data.draw_stage_card_number += 1

        def unregister(self):
            self.player.data.draw_stage_card_number -= 1


class Bouquet(BaseWeapon):
    def __init__(self, states=CardStateEnum, transitions=transtions):
        super().__init__(states=states, transitions=transitions)
        self.attack_distence = 1
        self.identity = WeaponIdentity.bouquet
        self.description = "You can discard a card and draw a card,twice per turn"

    class BouquetSkill(EquipmentSkill):
        def __init__(self, player):
            super().__init__(player=player)
            self.name = "BouquetSkill"
            self.description = "You can discard a card and draw a card,twice per turn"

        def discard_a_card_and_draw_a_card(self, card, drawpile, discard_pile):
            self.use_twice_in_turn()
            self.player.card_action.discard_card(card, discard_pile)
            self.player.card_action.draw_card(drawpile, 1)
