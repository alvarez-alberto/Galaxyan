import esper, random, pygame

from src.create.enemy_creator import create_bullet_enemy
from src.ecs.components.c_enemy_bullet_spawner import CEnemyBulletSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_bullet_enemy import CTagBulletEnemy
from src.ecs.components.tag.c_tag_enemy import CTagEnemy

def system_enemy_shoot(world:esper.World, bullet_data:dict, sp_bullet_entity: int, delta_time:float):
    components = world.get_components(CTransform, CSurface, CTagEnemy)

    component_bullet_spawn = world.component_for_entity(sp_bullet_entity, CEnemyBulletSpawner)

    component_bullet_spawn.current_time += delta_time

    if component_bullet_spawn.all_clean == True and component_bullet_spawn.start == False:
        component_bullet_spawn.max_bullets = random.randint(bullet_data["min_bullets"], bullet_data["max_bullets"])
        component_bullet_spawn.all_clean = False
        component_bullet_spawn.start = True

    if component_bullet_spawn.start == True and component_bullet_spawn.current_time >= component_bullet_spawn.start_time:

        time_next_attack = component_bullet_spawn.time_next_attack + component_bullet_spawn.start_time

        if component_bullet_spawn.current_time >= time_next_attack: 
            component_bullet_spawn.time_next_attack = random.uniform(component_bullet_spawn.time_attack_min, component_bullet_spawn.time_attack_max)
            component_bullet_spawn.current_time = component_bullet_spawn.start_time
        
            max_enemy_shoot = random.randint(0, bullet_data["max_enemy_shoot_same_time"])
            count = 0

            if component_bullet_spawn.max_bullets == 0:
                component_bullet_spawn.start = False
                return

            if max_enemy_shoot <= component_bullet_spawn.max_bullets:
                component_bullet_spawn.max_bullets = component_bullet_spawn.max_bullets - max_enemy_shoot

                if max_enemy_shoot != 0 and components.__len__() > 0:
                        enemies = []

                        for _ in range(max_enemy_shoot):
                            enemies.append(random.randint(1, components.__len__()))

                        for entity, (c_t, c_s, c_te) in components:
                            count += 1

                            if count in enemies:
                                area = c_s.area.copy()
                                posx = c_t.pos.x + area.w
                                posy = c_t.pos.y + area.h
                                position = pygame.Vector2(posx, posy)
                                create_bullet_enemy(world, bullet_data, position)
