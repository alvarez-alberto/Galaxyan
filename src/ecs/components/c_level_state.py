from enum import Enum


class LevelState(Enum):
    START = 0
    PLAY = 1
    PAUSED = 2

class CLevelState:
    def __init__(self, game_start_text:int) -> None:
        self.state:LevelState = LevelState.START
        self.state_time = 0
        self.time_game_start = 3

        self.game_start_text = game_start_text


