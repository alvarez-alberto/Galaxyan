
import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_player import CTagPlayer


def system_screen_player(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface, CTagPlayer )

    screen_rect = screen.get_rect()
    c_t:CTransform
    c_s:CSurface
    for player, (c_t,c_s,_) in components:

        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        min_x = 10
        max_x = screen_rect.width - 10

        c_t.pos.x = max(min(c_t.pos.x, max_x - player_rect.width), min_x)
