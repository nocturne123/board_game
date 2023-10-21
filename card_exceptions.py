class NeedTargetException(Exception):
    """需要目标的异常"""

    pass


class CardNotInHandStateException(Exception):
    """不在手牌中的异常"""

    pass


class CardNotInHandException(Exception):
    pass


class NeedFurtherTargetException(Exception):
    """需要进一步选择目标的异常"""

    pass


class ImmuneToAttackException(Exception):
    """免疫攻击的异常"""

    pass


class MismatchedCardException(Exception):
    """卡牌不匹配的异常，主要用于偷牌时，卡牌不在目标有效手牌或装备中"""

    pass
