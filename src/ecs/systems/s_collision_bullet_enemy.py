import esper, pygame

from src.create.explosion_creator import create_explosion

from src.create.util_creator import create_max_score_text, create_score_value
from src.ecs.components.c_score_high_text import CHighScoreText
from src.ecs.components.c_score_text import CScoreText
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_enemy(world: esper.World, explosion_cfg:dict, delete_bullet:bool) -> bool:
    componentsenemy = world.get_components(CSurface, CTransform, CTagEnemy)
    componentsbullet = world.get_components(CSurface, CTransform, CTagBullet)    
    components_text_high_score = world.get_components(CHighScoreText)
    components_score_text = world.get_components(CScoreText)

    for enemy_entity, (c_s, c_t, c_tge) in componentsenemy:
        ene_rect:pygame.Rect = CSurface.get_area_relative(c_s.area, c_t.pos)

        for bullet_entity, (c_sb, c_tb, c_tgb) in componentsbullet:
            bullet_rect:pygame.Rect = CSurface.get_area_relative(c_sb.area, c_tb.pos)
            
            if ene_rect.colliderect(bullet_rect):
                world.delete_entity(bullet_entity)
                delete_bullet = True
                world.delete_entity(enemy_entity)
                create_explosion(world, pygame.Vector2(ene_rect.x, ene_rect.y), explosion_cfg)
                
                for txt_entity, (c_cs_txt) in components_score_text:                                   
                    world.delete_entity(txt_entity)                    
                    new_high_score = ServiceLocator.score_service.update_score_player(c_tge.score)
                    create_score_value(world)
                    if new_high_score:
                        for txt_entity, (c_hs_txt) in components_text_high_score:
                            world.delete_entity(txt_entity)
                            create_max_score_text(world)
                            
                 
    
    return delete_bullet