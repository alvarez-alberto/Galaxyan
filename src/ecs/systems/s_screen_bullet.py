
import json
import esper
import pygame

from src.create.play_creator import create_bullet
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet



def system_screen_bullet(world:esper.World, screen:pygame.Surface,player_entity:int,bullet_cfg:dict, delete_bullet:bool, pl_entity:int, bullets_cfg:dict) -> bool:
    components = world.get_components(CTransform, CSurface, CVelocity,CBulletState,CTagBullet)

    screen_rect = screen.get_rect()
    c_t:CTransform
    c_s:CSurface
    c_v:CVelocity
    c_bs:CBulletState
    c_tag:CTagBullet

    if delete_bullet:
        create_bullet(world, pl_entity, bullets_cfg)
        delete_bullet = False

    for bullet_entity, (c_t, c_s, c_v,c_bs,c_tag) in components:
        
        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        outside = False
        outside_top = False
        if bullet_rect.left < 0 or bullet_rect.right > screen_rect.width:
            outside = True

        if bullet_rect.top < 0 or bullet_rect.bottom > screen_rect.height:
            outside_top = True

        if outside:
            bullet_rect.clamp_ip(screen_rect)
            c_t.pos.x = bullet_rect.x
            c_t.pos.y = bullet_rect.y
            
        if outside_top or c_bs.in_cannon:
            player_pos = world.component_for_entity(player_entity, CTransform)
            player_surface = world.component_for_entity(player_entity, CSurface)
            player_size = player_surface.area.size
            bullet_size = bullet_cfg["player"]["size"]                
            player_center_x = player_pos.pos.x + player_size[0] / 2                    
            bullet_x = player_center_x - bullet_size["w"] / 2                    
            bullet_y = player_pos.pos.y - bullet_size["h"]                    
            pos = pygame.Vector2(bullet_x, bullet_y) 
            c_t.pos = pos
            c_v.vel = pygame.Vector2(0,0)
            c_bs.in_cannon = True

    return delete_bullet
            




