import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.ecs.components.tag.c_tag_player import CTagPlayer

def system_movement(world:esper.World, delta_time:float):
    components = world.get_components(CTransform, CVelocity)

    c_t:CTransform
    c_v:CVelocity
    for entity, (c_t, c_v) in components:

        if world.has_component(entity, CTagEnemy):
            continue

        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time
