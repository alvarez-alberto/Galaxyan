from enum import Enum

class CExplosionState:
    def __init__(self) -> None:
        self.state = ExplosionState.IDLE

class ExplosionState(Enum):
    IDLE = 1