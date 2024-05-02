

from enum import Enum
import pygame

class CHunterState:
    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pos.copy()
        self.state = HunterState.IDLE 

class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2