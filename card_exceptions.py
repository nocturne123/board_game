class NeedTargetException(Exception):
    """需要目标的异常"""

    pass


class NotInHandStateException(Exception):
    """不在手牌中的异常"""

    pass


class NeedFurtherTargetException(Exception):
    """需要进一步选择目标的异常"""

    pass
