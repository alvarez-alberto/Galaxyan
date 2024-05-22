import pygame

class CLevelText:
    def __init__(self, level: int, font:pygame.font.Font, color:pygame.Color, pos:pygame.Vector2) -> None:
        self.level = level
        self.font = font
        self.color = color
        self.pos = pos