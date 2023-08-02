from charaters import Charater
from ENUMS import CharaterAliveEnum


class Player:
    def __init__(self, cha: Charater):
        self.health = cha.health
        self.speed = cha.speed
        self.skills = None

        #玩家的武器、护甲均为空列表形式，因为红龙能装多个装备，设计为列表也方便未来的扩展
        self.armor = []
        self.weapon = []

        #玩家手牌
        self.hand_sequence = []

        #玩家收集品
        self.colloctions = []

        #玩家可否被选中，主要针对特殊状态，例如晕眩、针线提供的无敌、余晖烁烁的无敌、王冠提供的无敌
        self.is_selectable = True

        #玩家id，未来看是否会用到
        self.id = 0

        #角色的三种基本攻击
        self.physical_attack = cha.physical_attack
        self.magic_attack = cha.magic_attack
        self.mental_attack = cha.mental_attack

        #角色的基础生命值和最大生命值
        self.base_health = cha.health
        self.max_health = cha.health

        #角色在回合开始时的抽牌数量
        self.draw_stage_card_number = 2

        #角色初始手牌数量
        self.start_game_draw = 4

        #以下4个属性为能否使用卡牌和能否装备卡牌，用来解决角色是否有出牌阶段和
        #能否出牌的问题，玩家类里面对能否出牌进行判断，game类对是否有出牌阶段进行判断
        self.able_to_use_card = True
        self.able_to_equip = True
        self.have_draw_card_stage = True
        self.have_use_card_stage = True

        #角色最大手牌数量
        self.max_hand_sequence = 6

        #玩家移动次数
        self.move_chance = 1

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
        if self.able_to_use_card:
            pass
        if target.is_selectable:
            card.take_effect(self, target)
            self.hand_sequence.remove(card)

    def get_damage(self, damage_pack):
        self.health -= damage_pack[0]

    def draw_card(self,pile):
        
        for i in range(self.draw_stage_card_number):
            self.hand_sequence.append(pile.pop())

    def first_round_draw(self,pile):
        for i in range(self.start_game_draw):
            self.hand_sequence.append(pile.pop())
