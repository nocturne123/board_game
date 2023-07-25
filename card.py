from ENUMS import CardTypeEnum

#牌类简易实现，现阶段只实现了牌的类型分类

class Card:
    def __init__(self,card_type):
        self.type = card_type