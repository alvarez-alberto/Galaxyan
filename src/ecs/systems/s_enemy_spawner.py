
import esper
import pygame
from src.create.util_creator import crear_enemigo, create_hunter
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemySpawnEvent

def system_enemy_spawner(world:esper.World, enemy_data:dict, delta_time:float ):
    components = world.get_component(CEnemySpawner)

    c_enemyspw:CEnemySpawner
    for entity, c_enemyspw in components:

        c_enemyspw.time_spawn += delta_time

        event_spawn: EnemySpawnEvent

        for event_spawn in c_enemyspw.spawn_events:
            if event_spawn.time < c_enemyspw.time_spawn and not event_spawn.created:
                                
                new_enemy_info = enemy_data[event_spawn.enemy_type]
                pos = event_spawn.position
                

                if(event_spawn.enemy_type != "Hunter"):
                    crear_enemigo(world,new_enemy_info,pos)
                
                else:
                    velocity = pygame.Vector2(0,0)
                    create_hunter(world,pos,velocity,new_enemy_info)

                    

                event_spawn.created = True

   

        