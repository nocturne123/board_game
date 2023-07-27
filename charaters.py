import toml

# 角色简易实现
# TODO:实现基于toml的角色导入导出


class Charater:
    def __init__(self, health, magic_attack, physical_attack, mental_attack, speed):
        self.health = health
        self.magic_attack = magic_attack
        self.physical_attack = physical_attack
        self.mental_attack = mental_attack
        self.speed = speed
        self.collect_items = tuple()


# 测试代码：实例化一个big_mac
# big_mac = Charater(15, 0, 3, 0, 1)
