
import esper
import pygame

from src.create.enemy_creator import create_enemy
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemySpawnEvent

def system_enemy_spawner(world:esper.World, enemy_data:dict, delta_time:float):
    components = world.get_component(CEnemySpawner)

    c_enemyspw:CEnemySpawner
    for entity, c_enemyspw in components:

        c_enemyspw.time_spawn += delta_time

        event_spawn: EnemySpawnEvent

        for event_spawn in c_enemyspw.spawn_events:
            if event_spawn.time < c_enemyspw.time_spawn and not event_spawn.created:
                
                pos:pygame.Vector2 = event_spawn.position
                posx_original = pos.x

                for row in range(event_spawn.rows):
                    if row  != 0:
                        pos = pygame.Vector2(posx_original, pos.y + event_spawn.spacing_between_rows)

                    for column in range(event_spawn.columns):
                        if column != 0:
                            pos = pygame.Vector2(pos.x + event_spawn.spacing_between_columns, pos.y)

                        new_enemy_info = enemy_data[event_spawn.enemy_type]
                        create_enemy(world, pos, new_enemy_info, enemy_data)
                        event_spawn.created = True
