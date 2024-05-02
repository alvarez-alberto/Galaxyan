

import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.ecs.components.tag.c_tag_special_bullet import CTagSpecialBullet

def system_collision_bullet_enemy(world:esper.World, explosion_cfg: dict):

    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)

    bullet_c_s:CSurface
    bullet_c_t:CTransform
    for bullet_entity, (bullet_c_s, bullet_c_t, _) in components_bullet:

        bullet_rect = CSurface.get_area_relative(bullet_c_s.area, bullet_c_t.pos)

        enemy_c_s: CSurface
        enemy_c_t: CTransform
        for enemy_entity, (enemy_c_s, enemy_c_t, _) in components_enemy:
            enemy_rect = CSurface.get_area_relative(enemy_c_s.area, enemy_c_t.pos)

            if bullet_rect.colliderect(enemy_rect):
                create_explosion(world, enemy_c_t.pos, explosion_cfg)
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)

       

