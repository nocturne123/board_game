from collections import deque
from ENUMS.common_enums import CharaterAliveEnum
from player import Player
from player_data import PlayerData
from charaters import Charater, SpeciesEnum


class Team(deque[Player]):
    def __init__(self, maxlen):
        super().__init__(maxlen=maxlen)

    @property
    def active_member(self):
        return self[0]

    @property
    def is_remaining(self):
        return any(
            player.data.living_state != CharaterAliveEnum.dead for player in self
        )

    def next_alive_player(self):
        if self.is_remaining:
            while self[0].data.living_state == CharaterAliveEnum.dead:
                a = self.popleft()
                self.append(a)
        else:
            pass

    def alive_list(self):
        return [
            player
            for player in self
            if player.data.living_state != CharaterAliveEnum.dead
        ]

    def __repr__(self) -> str:
        return f"Team({[player.data.name for player in self]})"


if __name__ == "__main__":
    big_mac = Charater(
        health=15,
        magic_attack=0,
        physical_attack=3,
        mental_attack=0,
        speed=1,
        name="big_mac",
        collect_items=(1, 2, 3),
        species=SpeciesEnum.earth_pony,
    )

    dummy = Charater(
        health=15,
        magic_attack=0,
        physical_attack=3,
        mental_attack=0,
        speed=1,
        name="dummy",
        collect_items=(1, 2, 3),
        species=SpeciesEnum.earth_pony,
    )

    mac_player = Player(PlayerData(big_mac))
    dummy_player = Player(PlayerData(dummy))
    b = Team(maxlen=2)
    b.extend([mac_player, dummy_player])
    print(b)
