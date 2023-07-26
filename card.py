from ENUMS import CardTypeEnum
import abc
from player import Player

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
    
    @property
    def card_type(self):
        return CardTypeEnum.physical_attack
    
    @property
    def take_effect(self,attack,target):
        damage = attack[1]
        target.get_damage((damage,attack))
