from functools import wraps


class UseOnceInTurn:
    def __init__(self, skill_use):
        self.skill_use = skill_use
        self.count = 1

    def __call__(self, *args, **kwargs):
        if self.count > 0:
            self.count -= 1
            return self.skill_use(*args, **kwargs)
        else:
            raise Exception("技能一轮只能使用一次")


class TestPlayer:
    def __init__(self) -> None:
        self.turn_count = 0

    def turn_start(self):
        self.turn_count += 1

    # 构造装饰器
    def use_once_in_turn(func):
        # 回合记录，使用技能前如果记录的回合和玩家回合相同，
        # 那么玩家在此回合已经使用过了技能，不能再使用
        # 如果不同，则使用技能，在技能结算完后将回合数更新到记录里
        turn_record = 0

        def wrapper(self, *args, **kwargs):
            nonlocal turn_record
            if turn_record != self.turn_count:
                turn_record = self.turn_count
                return func(self, *args, **kwargs)
            else:
                raise Exception("技能一轮只能使用一次")

        return wrapper

    @use_once_in_turn
    def some_skill(self):
        print("使用了一个技能")


player1 = TestPlayer()
player1.turn_start()
player1.some_skill()
player1.some_skill()
