from ENUMS import CardTypeEnum
import abc

#牌类简易实现，现阶段只实现了牌的类型分类

class Card(metaclass=abc.ABCMeta):
    
    @abc.abstractclassmethod
    def card_type(self) -> CardTypeEnum:
        return CardTypeEnum
    @abc.abstractclassmethod
    def take_effect(self,attack,target):
        pass

#物理攻击卡牌类
class PhysicalAttackCard(Card):
    
    
    def card_type(self):
        return CardTypeEnum.physical_attack
    
    
    def take_effect(self,card_user,target):
        damage = card_user.attack[1]
        target.get_damage((damage,card_user))

    def __repr__(self) -> str:
        return "physical attack"

#魔法攻击类卡牌
class MagicAttackCard(Card):
    
    
    def card_type(self):
        return CardTypeEnum.magic_attack
    
    
    def take_effect(self,card_user,target):
        damage = card_user.attack[0]
        target.get_damage((damage,card_user,self))

    def __repr__(self) -> str:
        return "magic attack"
    
#心理攻击类卡牌
class MentalAttackCard(Card):
    
    
    def card_type(self):
        return CardTypeEnum.mental_attack
    
    
    def take_effect(self,card_user,target):
        damage = card_user.attack[2]
        target.get_damage((damage,card_user,self))

    def __repr__(self) -> str:
        return "mental attack"