import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet

def system_fire_bullet(world:esper.World, vel:float):
    for bullet_entity, _ in world.get_component(CTagBullet):
        bullet_entity_vel = world.component_for_entity(bullet_entity, CVelocity)
        bullet_entity_vel.vel = pygame.Vector2(0,-vel)
   