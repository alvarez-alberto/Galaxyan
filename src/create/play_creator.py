import json

import pygame
import esper
from src.create.util_creator import create_sprite
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(ecs_world: esper.World):
    with open("assets/cfg/player.json", encoding="utf-8") as player_config:
            player_cfg = json.load(player_config)

    surface = ServiceLocator.images_service.get(player_cfg["image"])
    pos = pygame.Vector2(player_cfg["pos"]["x"],  
                         player_cfg["pos"]["y"])
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(ecs_world, pos, vel, surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    ecs_world.add_component(player_entity, CPlayerState())
    player_tr = ecs_world.component_for_entity(player_entity, CTransform)
    player_v = ecs_world.component_for_entity(player_entity, CVelocity)
    player_tag = ecs_world.component_for_entity(player_entity, CTagPlayer)
    player_state = ecs_world.component_for_entity(player_entity, CPlayerState)
    return (player_entity, player_tr, player_v, player_tag, player_state)