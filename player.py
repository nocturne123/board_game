from charaters import Charater
from ENUMS import CharaterAliveEnum


class Player:
    def __init__(self, cha: Charater):
        self.health = cha.health
        self.skills = None
        self.armor = []
        self.weapon = []
        self.hand_sequence = []
        self.colloctions = []
        self.is_selectable = True
        self.id = 0
        self.physical_attack = cha.physical_attack
        self.magic_attack = cha.magic_attack
        self.mental_attack = cha.mental_attack
        self.base_health = cha.health
        self.max_health = cha.health
        self.draw_stage_card_number = 2
        self.start_game_draw = 4

    @property
    def living_status(self):
        if self.health > 0:
            return CharaterAliveEnum.alive
        else:
            return CharaterAliveEnum.dead

    @property
    def attack(self):
        if self.weapon:
            magic_attack = self.attack + self.weapon.magic_attack
            physical_attack = self.weapon.physical_attack
            mental_attack = self.weapon.mental_attack
            return [magic_attack, physical_attack, mental_attack]
        else:
            return [self.magic_attack, self.physical_attack, self.mental_attack]

    # 打出卡牌，卡牌对目标生效，需要经过game类吗？
    # 如果需要经过game类，会不会太复杂了？game类职责是主持回合，需不需要经手卡牌的检测？应该是需要的
    # 这里是不经过game类的实现
    def use_card(self, card, target):
        if target.is_selectable:
            card.take_effect(self, target)
            self.hand_sequence.remove(card)

    def get_damage(self, damage_pack):
        self.health -= damage_pack[0]
