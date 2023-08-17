from collections import deque
from ENUMS import CharaterAliveEnum


class Team(deque):
    def __init__(self, maxlen):
        super().__init__(maxlen=maxlen)

    @property
    def active_member(self):
        return self[0]

    @property
    def is_remaining(self):
        return any(player.living_status != CharaterAliveEnum.dead for player in self)

    def next_alive_player(self):
        a = self.popleft()
        self.append(a)
        if self.is_remaining:
            while self[0].living_status == CharaterAliveEnum.dead:
                a = self.popleft()
                self.append(a)
        else:
            pass

    def alive_list(self):
        return [
            player for player in self if player.living_status != CharaterAliveEnum.dead
        ]


a = Team(maxlen=3)
a.extend(["a", "b", "c"])
print(a)
a.append("d")
print(a)
a.next_player()
print(a)
