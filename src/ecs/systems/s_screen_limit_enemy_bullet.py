import esper, pygame, random

from src.ecs.components.c_enemy_bullet_spawner import CEnemyBulletSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_bullet_enemy import CTagBulletEnemy


def system_screen_limit_enemy_bullet(world: esper.World, screen_rect: pygame.Rect, sp_bullet_entity: int):
    components = world.get_components(CTransform, CSurface, CTagBulletEnemy)

    component_bullet_spawn = world.component_for_entity(sp_bullet_entity, CEnemyBulletSpawner)

    c_t:CTransform
    c_s:CSurface

    for bullet_entity, (c_t, c_s, c_b) in components:
        bullet_rect:pygame.Rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            
        if bullet_rect.top < 0 or bullet_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)

    if components.__len__() <= 0 and component_bullet_spawn.current_time >= component_bullet_spawn.start_time and component_bullet_spawn.all_clean == False:
        component_bullet_spawn.all_clean = True
        component_bullet_spawn.current_time = 0.0
        component_bullet_spawn.start_time = random.uniform(component_bullet_spawn.time_attack_min, component_bullet_spawn.time_attack_max)
        component_bullet_spawn.time_next_attack = 0.0