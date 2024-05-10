import esper, pygame

from src.create.util_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_bullet_spawner import CEnemyBulletSpawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet_enemy import CTagBulletEnemy
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

def create_spawn_enemy_bullet(ecs_world: esper.World, bullet_data:dict) -> int:
    spawn_entity = ecs_world.create_entity()
    ecs_world.add_component(spawn_entity, CEnemyBulletSpawner(0, True, False, bullet_data["start_time"],
                                                              bullet_data["time_attack_min"],
                                                              bullet_data["time_attack_max"]))
    return spawn_entity

def create_bullet_enemy(ecs_world: esper.World, bullet_enemy_info:dict, position_enemy: pygame.Vector2):
    bullet_enemy_entity = ecs_world.create_entity()
    ecs_world.add_component(bullet_enemy_entity, CSurface(pygame.Vector2(bullet_enemy_info["size"]["w"], 
                                                                         bullet_enemy_info["size"]["h"]),
                                                            pygame.Color(bullet_enemy_info["color"]["r"],
                                                                         bullet_enemy_info["color"]["g"],
                                                                         bullet_enemy_info["color"]["b"])))
    ecs_world.add_component(bullet_enemy_entity, CTransform(position_enemy))
    ecs_world.add_component(bullet_enemy_entity, CVelocity(pygame.Vector2(0, bullet_enemy_info["velocity"])))
    ecs_world.add_component(bullet_enemy_entity, CTagBulletEnemy())