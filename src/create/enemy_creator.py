import esper, pygame

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def create_enemy(ecs_world: esper.World, position: pygame.Vector2, enemy_info:dict, enemy_data:dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocityx = enemy_data["velocity_start"]
    velocityy = 0
    velocity = pygame.Vector2(velocityx, velocityy)
    enemy_entity = create_sprite(ecs_world, position, velocity, enemy_surface)
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ecs_world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))

def create_spawn(ecs_world: esper.World, events_data:dict):
    spawn_entity = ecs_world.create_entity()
    ecs_world.add_component(spawn_entity, CEnemySpawner(events_data))
