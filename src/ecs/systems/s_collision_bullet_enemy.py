import esper, pygame

from src.create.explosion_creator import create_explosion

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(world: esper.World, explosion_cfg:dict, delete_bullet:bool) -> bool:
    componentsenemy = world.get_components(CSurface, CTransform, CTagEnemy)
    componentsbullet = world.get_components(CSurface, CTransform, CTagBullet)

    for enemy_entity, (c_s, c_t, c_tge) in componentsenemy:
        ene_rect:pygame.Rect = CSurface.get_area_relative(c_s.area, c_t.pos)

        for bullet_entity, (c_sb, c_tb, c_tgb) in componentsbullet:
            bullet_rect:pygame.Rect = CSurface.get_area_relative(c_sb.area, c_tb.pos)
            
            if ene_rect.colliderect(bullet_rect):
                world.delete_entity(bullet_entity)
                delete_bullet = True
                world.delete_entity(enemy_entity)
                create_explosion(world, pygame.Vector2(ene_rect.x, ene_rect.y), explosion_cfg)
    
    return delete_bullet