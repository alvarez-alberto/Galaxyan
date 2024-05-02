import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_enemy import CTagEnemy

def system_screen_enemy(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)

    screen_rect = screen.get_rect()
    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    for entity, (c_t, c_v, c_s, c_e) in components:
        
        enemy_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if enemy_rect.left < 0 or enemy_rect.right > screen_rect.width:
            c_v.vel.x *= -1
            enemy_rect.clamp_ip(screen_rect)
            c_t.pos.x = enemy_rect.x

        if enemy_rect.top < 0 or enemy_rect.bottom > screen_rect.height:
            c_v.vel.y *= -1
            enemy_rect.clamp_ip(screen_rect)
            c_t.pos.y = enemy_rect.y