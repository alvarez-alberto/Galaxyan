import json

import pygame
import esper
from src.create.util_creator import create_sprite, create_text
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_card_slice import CCardSlice
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator




def create_card_slice(ecs_world:esper.World, entity):
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    card_config = interface_cfg["card"]

    vel = card_config["vel"]
    outside = card_config["outside"]
    pos = ecs_world.component_for_entity(entity,CTransform).pos.copy()
    ecs_world.add_component(entity, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(entity, CCardSlice(vel, pos.y+outside, pos.y))



     
def create_title(ecs_world:esper.World) -> int:

    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")

    menu_cfg = interface_cfg["menu"]
    
    image = ServiceLocator.images_service.get(menu_cfg["image"])
    vel = pygame.Vector2(0,0)
    pos = pygame.Vector2(menu_cfg["pos"]["x"] - (image.get_width() / 2), 
                         menu_cfg["pos"]["y"])

    title_entity = create_sprite(ecs_world, pos, vel, image)

    return title_entity

def create_start_game_text(ecs_world: esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["title_text_color"]["r"],
                                          menu_cfg["title_text_color"]["g"],
                                          menu_cfg["title_text_color"]["b"])
    pos = pygame.Vector2(60,160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    press_start_entity = create_text(ecs_world, "PRESS Z TO START", font, color, pos)
    ecs_world.add_component(press_start_entity, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(press_start_entity, CBlink(0.5))
    return press_start_entity