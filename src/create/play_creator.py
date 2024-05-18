import json

import pygame
import esper
from src.create.util_creator import create_sprite
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(ecs_world: esper.World):
    with open("assets/cfg/player.json", encoding="utf-8") as player_config:
            player_cfg = json.load(player_config)

    surface = ServiceLocator.images_service.get(player_cfg["image"])
    pos = pygame.Vector2(player_cfg["pos"]["x"],  
                         player_cfg["pos"]["y"])
    vel = pygame.Vector2(0, 0)
    player_input_velocity = player_cfg["input_velocity"]
    player_entity = create_sprite(ecs_world, pos, vel, surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    ecs_world.add_component(player_entity, CPlayerState(player_cfg["time_spawn"]))
    player_tr = ecs_world.component_for_entity(player_entity, CTransform)
    player_v = ecs_world.component_for_entity(player_entity, CVelocity)
    player_tag = ecs_world.component_for_entity(player_entity, CTagPlayer)
    player_state = ecs_world.component_for_entity(player_entity, CPlayerState)
    return (player_entity, player_tr, player_v, player_tag, player_state,player_input_velocity)

def create_bullet(ecs_world: esper.World,  player_entity: int, bullet_cfg: dict):
    
    player_surface_component = ecs_world.component_for_entity(player_entity, CSurface)
    player_pos = ecs_world.component_for_entity(player_entity, CTransform)

    player_size = player_surface_component.area.size 
    bullet_size = bullet_cfg["player"]["size"]
    color = pygame.color.Color(bullet_cfg["player"]["color"]["r"],bullet_cfg["player"]["color"]["g"],bullet_cfg["player"]["color"]["b"])
    player_center_x = player_pos.pos.x + player_size[0] / 2   

    bullet_x = player_center_x - bullet_size["w"] / 2
    bullet_y = player_pos.pos.y - bullet_size["h"] 
    pos = pygame.Vector2(bullet_x, bullet_y)   
    vel = pygame.Vector2(0,0)  

    bullet_entity =  ecs_world.create_entity()
    ecs_world.add_component(bullet_entity, CTransform(pos))
    ecs_world.add_component(bullet_entity, CVelocity(vel)) 
    ecs_world.add_component(bullet_entity,  CSurface(pygame.Vector2(bullet_size["w"], bullet_size["h"]), color))
    ecs_world.add_component(bullet_entity, CTagBullet()) 
    ecs_world.add_component(bullet_entity,CBulletState(in_cannon=True))
    bullet_v = ecs_world.component_for_entity(bullet_entity, CVelocity)
    