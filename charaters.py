import toml
from ENUMS import SpeciesEnum

# 角色简易实现
# TODO:实现基于toml的角色导入导出


class Charater:
    def __init__(
        self, health, magic_attack, physical_attack, mental_attack, speed, name, species
    ):
        self.health = health
        self.magic_attack = magic_attack
        self.physical_attack = physical_attack
        self.mental_attack = mental_attack
        self.speed = speed
        self.collect_items = tuple()
        self.name = name
        self.species = species


if __name__ == "__main__":
    # 测试代码：实例化一个big_mac
    # big_mac = Charater(15, 0, 3, 0, 1)

    dst_file = "new_toml_file.toml"

    big_mac = Charater(15, 0, 3, 0, 1, "big_mac", SpeciesEnum.earth_pony)
    dic_mac = {
        "Big Mac": {
            "health": 15,
            "magic_attack": 0,
            "physical_attack": 3,
            "mental_attack": 0,
            "speed": 1,
            "species": "earth pony",
        }
    }

    dummy_dic = {
        "dummy": {
            "health": 15,
            "magic_attack": 0,
            "physical_attack": 3,
            "mental_attack": 0,
            "speed": 1,
            "species": "earth pony",
        }
    }
    with open(dst_file, "w") as f:
        r = toml.dump(dic_mac, f)
        r1 = toml.dump(dummy_dic, f)
