"""这个文件是卡牌的上级操作文件，包括抽牌、卡牌的使用、弃牌等卡牌自己看不到的操作"""
from player_action import PlayerAction
from player_data import PlayerData
from card_pile import DiscardPile, DrawPile
from ENUMS.common_enums import CardTypeEnum, CardStateEnum, PlayerStateEnum
from player_exceptions import (
    NotInPlayStateException,
    NoChanceToAttackException,
    ImmuneToAttackException,
    ImmuneToStealException,
)

from card_exceptions import (
    CardNotInHandStateException,
    CardNotInHandException,
    MismatchedCardException,
)


class CardAction:
    def __init__(self, player_action):
        self.player_action: PlayerAction = player_action
        self.data: PlayerData = self.player_action.data
        # 自动卸下装备的设置，当此项为真时，装上装备会自动卸下原有装备
        self.auto_unmount = True

    def draw_card(self, card_pile: DrawPile, num=1):
        """玩家抽牌"""
        for i in range(num):
            card = card_pile.pop()
            card.get_draw()
            card.get_into_hand()
            self.data.hand_sequence.append(card)

    def discard_card(self, card, discard_pile: DiscardPile):
        """玩家弃牌"""
        card.get_discarded()
        self.data.hand_sequence.remove(card)
        card.get_into_discard_pile()
        discard_pile.append(card)

    def use_card_checker(self, card, target):
        """检查卡牌是否合法"""
        # 检查玩家状态，只有在play状态下才能打出卡牌
        if self.data.stage_state.state != PlayerStateEnum.play:
            raise NotInPlayStateException
        # 检查卡牌是否在状态，你不能打出一张不在手牌状态的卡牌
        if card.state != CardStateEnum.in_hand:
            raise CardNotInHandStateException

        # 你不能打出一张不在手牌中的手牌
        if card not in self.data.hand_sequence:
            raise CardNotInHandException

        # 攻击牌下的检查
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            # 没有攻击次数时不能打出攻击牌
            if self.data.attack_chance_in_turn <= 0:
                raise NoChanceToAttackException
            # 目标免疫攻击时不能打出攻击牌
            if target.data.immune_from_attack:
                raise ImmuneToAttackException

        # 偷窃牌下的检查，目标免疫偷牌时无效
        # 注：target(Player,Card)，Player是被偷牌的目标，Card是被偷的牌
        if card.card_type == CardTypeEnum.steal:
            if target[0].data.immune_from_steal:
                raise ImmuneToStealException
            if (
                target[1] not in target[0].data.equipment_sequence
                and target[1] not in target[0].data.hand_sequence
            ):
                raise MismatchedCardException

    def use_card(
        self,
        card,
        target,  # 摆烂了，target可以为player，也可以是一个tuple[Player,Card]，如果想要类型提示的话一定会import player，但是这样就循环import了
        discard_pile: DiscardPile,
    ):
        """玩家使用卡牌，这个环节要包含卡牌的状态转换、卡牌的位置转换。
        卡牌自己产生的效果在卡牌的effect函数中实现，这里只调用effect函数，不关心效果的具体实现。
        当对自己使用卡牌，比如恢复牌、自我增益的效果牌时，target为None"""
        self.use_card_checker(card, target)  # 检查卡牌是否合法

        # 使用卡牌前的钩子函数
        if self.data.Hook_Before_Use:
            for func in self.data.Hook_Before_Use:
                func(self, card, target, discard_pile)
        card.get_played()
        self.data.hand_sequence.remove(card)  # 这个时刻，卡牌已经不在手牌中了

        # 当卡牌类型为攻击时，玩家的攻击次数减少1
        if (
            card.card_type == CardTypeEnum.physical_attack
            or card.card_type == CardTypeEnum.magic_attack
            or card.card_type == CardTypeEnum.mental_attack
        ):
            self.data.attack_chance_in_turn -= 1

        # 在这个阶段，视为已经指定了目标，并且把牌打出去了
        # 检查目标是否有被卡牌指定后的hook
        if target:
            if type(target) != tuple:  # 这是目标为Player的情况
                if target.data.Hook_After_Chosen:
                    for func in target.data.Hook_After_Chosen:
                        func(self, card, target, discard_pile)
            else:  # 这是目标为tuple的情况
                if target[0].data.Hook_After_Chosen:
                    for func in target[0].data.Hook_After_Chosen:
                        func(self, card, target, discard_pile)

        # 检查玩家是否有在卡牌生效前的hook
        if self.data.Hook_Before_Effect:
            for func in self.data.Hook_Before_Effect:
                func(self, card, target, discard_pile)

        # 检查目标是否有在卡牌生效前的hook
        if target:
            if type(target) != tuple:  # 这是目标为Player的情况
                if target.data.Hook_Before_Effect_As_Target:
                    for func in target.data.Hook_Before_Effect_As_Target:
                        func(self, card, target, discard_pile)
            else:  # 这是目标为tuple的情况
                if target[0].data.Hook_Before_Effect_As_Target:
                    for func in target[0].data.Hook_Before_Effect_As_Target:
                        func(self, card, target, discard_pile)

        # 当卡牌类型为装备时，状态转换逻辑要分开
        if (
            card.card_type == CardTypeEnum.armor
            or card.card_type == CardTypeEnum.weapon
            or card.card_type == CardTypeEnum.element
            or card.card_type == CardTypeEnum.anti_element
        ):
            card.get_equipped()  # 装备卡牌的状态转换，由on_use转换到on_equipment

            # 如果装备栏里已有装备，那么自动卸下原来的装备
            if self.auto_unmount:
                if card.card_type == CardTypeEnum.armor:
                    if self.data.armor_slot:
                        # 利用列表推导式找到装备栏里的装备
                        equiped_armor = [
                            i
                            for i in self.data.equipment_sequence
                            if i.card_type == CardTypeEnum.armor
                        ][0]
                        self.unmount_item(equiped_armor, discard_pile)
                elif card.card_type == CardTypeEnum.weapon:
                    if self.data.weapon_slot:
                        equiped_weapon = [
                            i
                            for i in self.data.equipment_sequence
                            if i.card_type == CardTypeEnum.weapon
                        ][0]
                        self.unmount_item(equiped_weapon, discard_pile)
                elif (
                    card.card_type == CardTypeEnum.element
                    or card.card_type == CardTypeEnum.anti_element
                ):
                    if self.data.element_slot:
                        equiped_element = [
                            i
                            for i in self.data.equipment_sequence
                            if (
                                i.card_type == CardTypeEnum.element
                                or i.card_type == CardTypeEnum.anti_element
                            )
                        ]
                        self.unmount_item(equiped_element, discard_pile)

            self.data.equipment_sequence.append(card)
            card.use(self, target)
            match card.card_type:
                case CardTypeEnum.armor:
                    self.data.armor_slot = True
                case CardTypeEnum.weapon:
                    self.data.weapon_slot = True
                case CardTypeEnum.element, CardTypeEnum.anti_element:
                    self.data.element_slot = True

        else:  # 一般卡牌的状态转换逻辑
            card.take_effect()  # 卡牌的状态转换，由on_use转换到on_taking_effect
            # 如果造成了伤害，那么造成伤害的值会一路从目标的received_damage传到
            # card的effect，传到card的use，最后传到这里
            dealed_damage_int = card.use(self, target)
            if dealed_damage_int:
                self.player_action.dealed_damage(dealed_damage_int)
            card.end_effect()  # 卡牌的状态转换，由on_taking_effect转换到on_discard
            card.get_into_discard_pile()  # 卡牌的状态转换，由on_discard转换到in_discard_pile
            discard_pile.append(card)
            return dealed_damage_int

        # 这个阶段，卡牌已经生效完毕，检查目标是否有被卡牌生效后的hook
        if target:
            if type(target) != tuple:  # 这是目标为Player的情况
                if target.data.Hook_After_Effect_As_Target:
                    for func in target.data.Hook_After_Effect_As_Target:
                        func(self, card, target, discard_pile)
            else:  # 这是目标为tuple的情况
                if target[0].data.Hook_After_Effect_As_Target:
                    for func in target[0].data.Hook_After_Effect_As_Target:
                        func(self, card, target, discard_pile)

        # 使用卡牌后的钩子函数
        if self.data.Hook_After_Use:
            for func in self.data.Hook_After_Use:
                func(self, card, target, discard_pile)

    def unmount_item(self, card, discard_pile: DiscardPile):
        """玩家卸下物品"""
        card.get_unmounted()  # 物品的状态转换，由on_equipment转换到on_discard
        card.unequiped(self)  # 调用卡牌的unequip函数，进行一些注销的操作
        self.data.equipment_sequence.remove(card)
        match card.card_type:
            case CardTypeEnum.armor:
                self.data.armor_slot = False
            case CardTypeEnum.weapon:
                self.data.weapon_slot = False
            case CardTypeEnum.element, CardTypeEnum.anti_element:
                self.data.element_slot = False
        card.get_into_discard_pile()
        discard_pile.append(card)
