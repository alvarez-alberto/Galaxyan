import json

import pygame
import esper
from src.create.prefab_creator import create_sprite, create_text
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def load_config_interface() -> dict:
        with open("assets/cfg/interface.json", encoding="utf-8") as interface_config:
            interface_cfg = json.load(interface_config)
        
        return interface_cfg
     
def create_title(ecs_world:esper.World):

    interface_cfg = load_config_interface()

    menu_cfg = interface_cfg["menu"]
    
    image = ServiceLocator.images_service.get(menu_cfg["image"])
    vel = pygame.Vector2(0,0)
    pos = pygame.Vector2(menu_cfg["pos"]["x"] - (image.get_width() / 2), 
                         menu_cfg["pos"]["y"])

    title_entity = create_sprite(ecs_world, pos, vel, image)

def create_start_game_text(ecs_world: esper.World) -> None:
    interface_cfg = load_config_interface()
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["color"]["r"],
                                          menu_cfg["color"]["g"],
                                          menu_cfg["color"]["b"])
    pos = pygame.Vector2(60,160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    press_start_entity = create_text(ecs_world, "PRESS Z TO START", font, color, pos)
    ecs_world.add_component(press_start_entity, CVelocity(pygame.Vector2(0,0)))
