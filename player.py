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

    @property
    def base_health(self, cha):
        return cha.health

    @property
    def living_status(self):
        if self.health > 0:
            return CharaterAliveEnum.alive
        else:
            return CharaterAliveEnum.dead

    # base
    @property
    def attack(self, cha):
        if self.weapon:
            magic_attack = cha.magic_attack + self.weapon.magic_attack
            physical_attack = cha.physical_attack + self.weapon.physical_attack
            mental_attack = cha.mental_attack + self.weapon.mental_attack
            return [magic_attack, physical_attack, mental_attack]
        else:
            return [cha.magic_attack, cha.physical_attack, cha.mental_attack]
