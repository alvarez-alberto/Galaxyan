import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_player import CTagPlayer

def system_movement_player(world:esper.World, delta_time:float):
    components = world.get_components(CTransform, CVelocity, CTagPlayer)
    components2 = world.get_components(CTransform, CVelocity, CTagBullet)

    c_t:CTransform
    c_v:CVelocity
    for entity, (c_t, c_v, c_tgp) in components:
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time
    
    for entity, (c_t, c_v, c_tgb) in components2:
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time