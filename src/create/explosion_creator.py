import esper, pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explosion_state import CExplosionState
from src.engine.service_locator import ServiceLocator
from src.create.util_creator import create_sprite

def create_explosion(ecs_world: esper.World, position: pygame.Vector2, explosion_info:dict):
    explotion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    velocity = pygame.Vector2(0, 0)
    explotion_entity = create_sprite(ecs_world, position, velocity, explotion_surface)
    ecs_world.add_component(explotion_entity, CAnimation(explosion_info["animations"]))
    ecs_world.add_component(explotion_entity, CExplosionState())
    ServiceLocator.sounds_service.play(explosion_info["sound"])