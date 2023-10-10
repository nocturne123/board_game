class NotInPlayStateException(Exception):
    """玩家不在出牌状态的异常"""

    pass


class NoChanceToAttackException(Exception):
    """没有攻击机会的异常"""

    pass
