<<<<<<< Updated upstream

if message == 'a':
    #卡牌生效前的操作


if message =='b':
    #替换卡牌的操作
    for func in [funcs]:
        func()
else:
    #正常卡牌生效的操作

if message == 'c':
    #卡牌生效后的操作
=======
class Skill:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    @staticmethod
    def give_a(i):
        i.num += 1

    def hook_in(self, m):
        m.skill.append(self.give_a)


class ent:
    def __init__(self) -> None:
        self.skill = []
        self.num = 0

    def hooks(self):
        if self.skill:
            for i in self.skill:
                i(self)


a = ent()
b = Skill("a", 1)
b.hook_in(a)
a.hooks()
print(a.num)
>>>>>>> Stashed changes
