"""最基础的技能模块，所有技能都需要register功能和unregister功能，主动技能需要额外提供use功能"""
"""角色获得技能时，技能用connect连接上角色，再注册，使技能生效。
角色失去技能时，用disconnect断开连接，再注销，使技能失效。
技能被沉默时，调用unregister，使技能失效。
失效效果结束后，再调用register，使技能生效。"""
from player import Player
from card import Card
from abc import abstractclassmethod


class Skill:
    def __init__(self):
        # 是否被沉默，如果玩家被沉默则挂起，等沉默结束后再注册
        self.hold = False

    @abstractclassmethod
    def use(self, user: Player, target):
        pass

    def register(self, user: Player):
        pass

    def unregister(self, user: Player):
        pass

    def connect_player(self, user: Player):
        self.register(user)

    def disconnect_player(self, user: Player):
        self.unregister(user)


class CharacterSkill(Skill):
    """角色技能"""

    def __init__(self):
        super().__init__()

    def register(self, user: Player):
        user.data.character_skills.append(self)

    def unregister(self, user: Player):
        user.data.character_skills.remove(self)

    @abstractclassmethod
    def use(self, user: Player, target):
        pass


class EquipmentSkill(Skill):
    """装备技能"""

    def __init__(self):
        super().__init__()

    def register(self, user: Player):
        user.data.equipment_skills.append(self)

    def unregister(self, user: Player):
        user.data.equipment_skills.remove(self)

    @abstractclassmethod
    def use(self, user: Player, target):
        pass


class SpeciesSkill(Skill):
    """种族技能"""

    def __init__(self):
        super().__init__()

    def register(self, user: Player):
        user.data.species_skills.append(self)

    def unregister(self, user: Player):
        user.data.species_skills.remove(self)

    @abstractclassmethod
    def use(self, user: Player, target):
        pass
