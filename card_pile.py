"""牌堆的实现，继承自list，包含洗牌功能，对牌堆的操作在玩家类中实现"""
from random import shuffle


# TODO:实现抽牌，弃牌，洗牌等功能
class CardPile(list):
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return f"...{self[-3:]}({len(self)})"


class DrawPile(CardPile):
    def __init__(self):
        super().__init__()


'''
    def test_draw_pile(self):
        """临时测试的牌堆"""
        a = [PhysicalAttackCard() for i in range(16)]
        b = [MagicAttackCard() for i in range(16)]
        c = [MentalAttackCard() for i in range(16)]
        self.extend(a)
        self.extend(b)
        self.extend(c)
        shuffle(self)
'''


class DiscardPile(CardPile):
    def __init__(self):
        super().__init__()
