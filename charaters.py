import toml


class Charater:
    def __init__(self, health, magic_attack, physical_attack, mental_attack, speed):
        self.health = health
        self.magic_attack = magic_attack
        self.physical_attack = physical_attack
        self.mental_attack = mental_attack
        self.speed = speed
        self.collect_items = tuple()


big_mac = Charater(15, 0, 3, 0, 1)
