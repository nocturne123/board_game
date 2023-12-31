from player_data import PlayerData
from card_action import CardAction
from player_action import PlayerAction


class Player:
    def __init__(self, character) -> None:
        self.data: PlayerData = PlayerData(character)
        self.player_action = PlayerAction(self.data)
        self.card_action = CardAction(self.player_action)
