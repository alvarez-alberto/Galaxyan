
import esper
import pygame

from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_player import CTagPlayer


def system_screen_player(world:esper.World, screen:pygame.Surface,bullet_size:dict):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)

    screen_rect = screen.get_rect()
    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    for entity, (c_t, c_v, c_s, c_p) in components:
        
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        
        outside = False
        if player_rect.left < 0 or player_rect.right > screen_rect.width:
            outside = True

        # if player_rect.top < 0 or player_rect.bottom > screen_rect.height:
        #     outside = True

        if outside:
            player_rect.clamp_ip(screen_rect)
            c_t.pos.x = player_rect.x
            c_t.pos.y = player_rect.y
            for bullet_entity, (c_t_bullet,_) in world.get_components(CTransform,CTagBullet):
                    player_pos = world.component_for_entity(entity, CTransform)
                    player_size = c_s.area.size 
                    player_center_x = player_pos.pos.x + player_size[0] / 2  
                    bullet_x = player_center_x - bullet_size["w"] / 2
                    bullet_y = player_pos.pos.y - bullet_size["h"] 
                    pos = pygame.Vector2(bullet_x, bullet_y) 
                    c_t_bullet.pos = pos