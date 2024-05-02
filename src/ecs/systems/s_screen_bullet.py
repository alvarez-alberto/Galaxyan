
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet



def system_screen_bullet(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface, CTagBullet)

    screen_rect = screen.get_rect()
    c_t:CTransform
    c_s:CSurface
    for bullet_entity, (c_t, c_s, c_b) in components:
        
        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        outside = False
        if bullet_rect.left < 0 or bullet_rect.right > screen_rect.width:
            outside = True

        if bullet_rect.top < 0 or bullet_rect.bottom > screen_rect.height:
            outside = True

        if outside:
            world.delete_entity(bullet_entity)