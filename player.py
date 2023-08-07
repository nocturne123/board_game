from charaters import Charater
from ENUMS import CharaterAliveEnum, SpeciesEnum


class Player:
    def __init__(self, cha: Charater):
        self.health = cha.health
        self.speed = cha.speed
        self.skills = []
        self.name = cha.name
        self.species = cha.species

        # 玩家的武器、护甲均为空列表形式，因为红龙能装多个装备，设计为列表也方便未来的扩展
        self.armor = []
        self.weapon = []

        # 玩家手牌
        self.hand_sequence = []

        # 玩家收集品
        self.colloctions = []

        # 玩家可否被选中，主要针对特殊状态，例如晕眩、针线提供的无敌、余晖烁烁的无敌、王冠提供的无敌
        # 根据技能描述，线轴为不会受到伤害，余晖烁烁、王冠为不能成为攻击牌目标，增加不可被攻击选中的属性
        # 攻击不可被选中在攻击牌类种实现，玩家类仅提供属性
        # 玩家可否被偷窃，也写在这里
        self.is_selectable = True
        self.immune_from_attack = False
        self.immune_from_steal = False

        # 玩家id，未来看是否会用到
        self.id = 0

        # 角色的三种基本攻击
        self.physical_attack = cha.physical_attack
        self.magic_attack = cha.magic_attack
        self.mental_attack = cha.mental_attack

        # 角色的基础生命值和最大生命值
        self.base_health = cha.health
        self.max_health = cha.health

        # 角色在回合开始时的抽牌数量
        self.draw_stage_card_number = 2

        # 角色初始手牌数量
        self.start_game_draw = 4

        # 以下4个属性为能否使用卡牌和能否装备卡牌，用来解决角色是否有出牌阶段和
        # 能否出牌的问题，玩家类里面对能否出牌进行判断，game类对是否有出牌阶段进行判断
        self.able_to_use_card = False
        self.able_to_equip = False
        self.have_draw_card_stage = True
        self.have_use_card_stage = True

        # 角色最大手牌数量
        self.max_hand_sequence = 6

        # 玩家移动次数和攻击次数
        self.move_chance = 1
        self.attack_chance = 1

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
    # TODO 使用卡牌的逻辑需要详细设计
    def use_card(self, card, target):
        if self.able_to_use_card:
            if target.is_selectable:
                self.hand_sequence.remove(card)
                card.get_used(self,target)

            else:
                print(f"{target}无法被选中")
        else:
            print(f"{self.name}现在还不能出牌")

    def get_damage(self, damage_pack):
        self.health -= damage_pack[0]

    # 角色抽牌
    def draw_card(self, pile, num=1):
        if num <= 0:
            pass
        elif num == 1:
            self.hand_sequence.append(pile.pop())
        elif num > 1:
            for i in range(num):
                self.hand_sequence.append(pile.pop())

    # 角色弃牌
    def discard(self, discard_pile, card):
        if card in self.hand_sequence:
            self.hand_sequence.remove(card)
            discard_pile.append(card)
            return card

    def first_round_draw(self, pile):
        self.draw_card(pile, num=self.start_game_draw)
