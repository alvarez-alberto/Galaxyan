import json

import pygame
import esper
from src.create.util_creator import create_sprite, create_text
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_card_slice import CCardSlice
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def load_config_interface() -> dict:
        with open("assets/cfg/interface.json", encoding="utf-8") as interface_config:
            interface_cfg = json.load(interface_config)
        
        return interface_cfg


def create_card_slice(ecs_world:esper.World, entity):
    interface_cfg = load_config_interface()
    card_config = interface_cfg["card"]

    vel = card_config["vel"]
    outside = card_config["outside"]
    pos = pygame.Vector2(60,160)
    ecs_world.add_component(entity, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(entity, CCardSlice(vel, pos.y+outside, pos.y))



     
def create_title(ecs_world:esper.World):

    interface_cfg = load_config_interface()

    menu_cfg = interface_cfg["menu"]
    
    image = ServiceLocator.images_service.get(menu_cfg["image"])
    vel = pygame.Vector2(0,0)
    pos = pygame.Vector2(menu_cfg["pos"]["x"] - (image.get_width() / 2), 
                         menu_cfg["pos"]["y"])

    title_entity = create_sprite(ecs_world, pos, vel, image)

def create_start_game_text(ecs_world: esper.World) -> int:
    interface_cfg = load_config_interface()
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["color"]["r"],
                                          menu_cfg["color"]["g"],
                                          menu_cfg["color"]["b"])
    pos = pygame.Vector2(60,160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    press_start_entity = create_text(ecs_world, "PRESS Z TO START", font, color, pos)
    ecs_world.add_component(press_start_entity, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(press_start_entity, CBlink(0.5))
    return press_start_entity