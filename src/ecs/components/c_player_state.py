from enum import Enum


class CPlayerState:
    def __init__(self, time_spawn:float) -> None:
        self.state = PlayerState.IDLE
        self.is_dead = False
        self.lives = 3
        self.current_time = 0.0
        self.time_spawn = time_spawn

class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
        