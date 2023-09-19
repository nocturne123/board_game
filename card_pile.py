"""牌堆的实现，继承自list，包含洗牌功能，对牌堆的操作在玩家类中实现"""


# TODO:实现抽牌，弃牌，洗牌等功能
class CardPile(list):
    def __init__(self):
        super().__init__()


class DrawPile(CardPile):
    def __init__(self):
        super().__init__()

    def test_draw_pile(self):
        """临时测试的牌堆"""
        self.extend(
            [
                PhysicalAttackCard(),
                MagicAttackCard(),
                MentalAttackCard(),
            ]
            * 5
        )
        shuffle(self)


class DiscardPile(CardPile):
    def __init__(self):
        super().__init__()
