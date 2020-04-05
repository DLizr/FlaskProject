from src.player.Player import Player


class PlayerKickedException(Exception):
    def __init__(self, player: Player, reason: str):
        super().__init__()
        self.player = player
        self.reason = reason
