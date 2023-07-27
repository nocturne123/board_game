from random import shuffle
from card import PhysicalAttackCard,MagicAttackCard,MentalAttackCard

class BaseStage:
    def __init__(self):
        pass

#牌堆类
class CardPile:
    def __init__(self):
        self.card_list=[]
        
        
class DrawPile(CardPile):
    def __init__(self) -> None:
        self.card_list = [PhysicalAttackCard(),MagicAttackCard(),MentalAttackCard()]*5
        shuffle(self.card_list)


class Round:
    def __init__(self):
        pass

class Game:
    def __init__(self,*players):
        self.player_list=[*players]

