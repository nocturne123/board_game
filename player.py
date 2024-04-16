from player_data import PlayerData
from player_action import PlayerAction


class Player:
    def __init__(self, character) -> None:
        self.data: PlayerData = PlayerData(character)
        self.actions = PlayerAction(self.data)
