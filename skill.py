"""最基础的技能模块，所有技能都需要register功能和unregister功能，主动技能需要额外提供use功能"""
"""角色获得技能时，技能用connect连接上角色，再注册，使技能生效。
角色失去技能时，用disconnect断开连接，再注销，使技能失效。
技能被沉默时，调用unregister，使技能失效。
失效效果结束后，再调用register，使技能生效。"""

if __name__ == "__main__":
    from player import Player

from abc import abstractmethod


class Skill:
    def __init__(self, player: Player = None):
        # 是否被沉默，如果玩家被沉默则挂起，等沉默结束后再注册
        self.hold = False
        self.player = player
        self.registed = False
        self.register()

    # 主动技能需要额外提供use功能，
    # 被动技能的效果直接写在register和unregister里面，注册后生效
    def use(self, user: Player, target):
        pass

    @abstractmethod
    def register(self, user: Player):
        pass

    @abstractmethod
    def unregister(self, user: Player):
        pass


class CharacterSkill(Skill):
    """角色技能"""

    def __init__(self, player: Player):
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

    def __init__(self, player: Player):
        super().__init__(player=player)
        self.player.data.species_skills.append(self)
