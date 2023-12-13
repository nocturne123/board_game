"""最基础的技能模块，所有技能都需要register功能和unregister功能，主动技能需要额外提供use功能"""
"""角色获得技能时，技能用connect连接上角色，再注册，使技能生效。
角色失去技能时，用disconnect断开连接，再注销，使技能失效。
技能被沉默时，调用unregister，使技能失效。
失效效果结束后，再调用register，使技能生效。"""

if __name__ == "__main__":
    from player import Player

from abc import abstractmethod
from functools import wraps


class Skill:
    def __init__(self, player=None):
        # 是否被沉默，如果玩家被沉默则挂起，等沉默结束后再注册
        self.hold = False
        self.player = player
        self.registed = False
        self.register()
        # 回合记录
        self.turn_record = 0
        # 一个回合中的使用次数记录
        self.used_count_in_turn = 0
        # 轮次记录
        self.round_record = 0
        # 一轮中的使用次数记录
        self.used_count_in_round = 0

    # 主动技能需要额外提供use功能，
    # 被动技能的效果直接写在register和unregister里面，注册后生效
    def use(self, user, target):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def unregister(self):
        pass

    # 一些装饰器，用来限定技能
    # 包括一回合使用一次、一轮使用一次
    def use_once_in_turn(self):
        """限定技能一回合只能使用一次"""
        # 回合记录，使用技能前如果记录的回合和玩家回合相同，
        # 那么玩家在此回合已经使用过了技能，不能再使用
        # 如果不同，则使用技能，在技能结算完后将回合数更新到记录里

        if self.turn_record != self.player.data.turn_count:
            self.turn_record = self.player.data.turn_count
        else:
            raise Exception("技能一回合只能使用一次")

    def use_once_in_round(self):
        """限定技能一轮只能使用一次"""
        # 轮次记录，使用技能前如果记录的轮次和玩家轮次相同，
        # 那么玩家在此轮已经使用过了技能，不能再使用
        # 如果不同，则使用技能，在技能结算完后将轮次数更新到记录里
        if self.round_record != self.player.data.round_count:
            self.round_record = self.player.data.round_count
        else:
            raise Exception("技能一轮只能使用一次")

    def use_twice_in_turn(self):
        """限定技能一回合只能使用两次"""

        # 每回合的第一次使用，将回合记录更新为玩家回合数，使用次数更新为1
        if self.turn_record != self.player.data.turn_count:
            self.turn_record = self.player.data.turn_count
            self.used_count_in_turn = 1

        # 每回合不是第一次使用，使用次数加1
        elif self.turn_record == self.player.data.turn_count:
            if self.used_count_in_turn < 2:
                self.used_count_in_turn += 1
            else:
                raise Exception("技能一回合只能使用两次")


class CharacterSkill(Skill):
    """角色技能"""

    def __init__(self, player):
        super().__init__(player=player)
        # 在这一步添加到角色的技能列表里面
        self.player.data.character_skills.append(self)


class EquipmentSkill(Skill):
    """装备技能"""

    def __init__(self, player):
        super().__init__(player=player)
        self.player.data.equipment_skills.append(self)


class SpeciesSkill(Skill):
    """种族技能"""

    def __init__(self, player):
        super().__init__(player=player)
        self.player.data.species_skills.append(self)
