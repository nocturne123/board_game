from charaters import Charater
from ENUMS import CharaterAliveEnum


class Player:
    def __init__(self, cha: Charater):
        self.health = cha.health

    

    @property
    def base_health(self,cha):
        return cha.health
    
    @property
    def living_status(self):
        if self.health > 0:
            return CharaterAliveEnum.alive
        else:
            return CharaterAliveEnum.dead
    
    @property
    def hand_sequence(self):
        sequence = []
        return sequence

    @property
    def weapon(self):
        return None

    @property
    def armor(self):
        return None

    @property
    def collection(self):
        return None

    @property
    def skill_1(self):
        return None

    # base
    @property
    def attack(self, cha):
        if self.weapon:
            magic_attack = cha.magic_attack + self.weapon.magic_attack
            physical_attack = cha.physical_attack + self.weapon.physical_attack
            mental_attack = cha.mental_attack + self.weapon.mental_attack
            return [magic_attack,physical_attack,mental_attack]
        else:
            return [cha.magic_attack,cha.physical_attack,cha.mental_attack]
        
    
