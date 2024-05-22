
import pygame
import esper
from src.create.util_creator import create_sprite, create_text
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.tag.c_tag_lives import CTagLives
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(ecs_world: esper.World):
    player_cfg = ServiceLocator.configs_service.load_config("assets/cfg/player.json")
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

def create_player_lives(ecs_world: esper.World, level_info: dict):  
    surface = ServiceLocator.images_service.get(level_info["image"])
    pos = pygame.Vector2(level_info["position"]["x"], level_info["position"]["y"])
    vel = pygame.Vector2(0, 0)
    player_live = create_sprite(ecs_world, pos, vel, surface)
    ecs_world.add_component(player_live, CTagLives())
    return player_live

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


def create_game_start_text(ecs_world:esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["normal_text_color"]["r"],menu_cfg["normal_text_color"]["g"],menu_cfg["normal_text_color"]["b"])
    pos = pygame.Vector2(90, 160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    game_start_entity = create_text(ecs_world, "GAME START", font, color, pos)
    return game_start_entity    

def create_paused_text(ecs_world:esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["title_text_color"]["r"],menu_cfg["title_text_color"]["g"],menu_cfg["title_text_color"]["b"])
    pos = pygame.Vector2(110, 160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    pause_text_entity = create_text(ecs_world, "PAUSE", font, color, pos)
    pause_surface = ecs_world.component_for_entity(component_type=CSurface, entity=pause_text_entity)
    pause_surface.visible = False

    pause_blink = CBlink(0.5)

    ecs_world.add_component(pause_text_entity,pause_blink)
    pause_blink.active = False


    return pause_text_entity

def create_game_over_text(ecs_world:esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["normal_text_color"]["r"],menu_cfg["normal_text_color"]["g"],menu_cfg["normal_text_color"]["b"])
    pos = pygame.Vector2(90, 160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    game_over_text_entity = create_text(ecs_world, "GAME OVER", font, color, pos)
    return game_over_text_entity

def create_level_complete_text(ecs_world:esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["normal_text_color"]["r"],menu_cfg["normal_text_color"]["g"],menu_cfg["normal_text_color"]["b"])
    pos = pygame.Vector2(75, 160)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    level_complete_text_entity = create_text(ecs_world, "LEVEL COMPLETE", font, color, pos)
    level_complete_surface = ecs_world.component_for_entity(component_type=CSurface, entity=level_complete_text_entity)
    level_complete_surface.visible = False
    return level_complete_text_entity

def create_get_ready_text(ecs_world:esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
    menu_cfg = interface_cfg["menu"]
    color = pygame.color.Color(menu_cfg["title_text_color"]["r"],menu_cfg["title_text_color"]["g"],menu_cfg["title_text_color"]["b"])
    pos = pygame.Vector2(20, 180)
    font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

    get_ready_text_entity = create_text(ecs_world, "GET READY FOR THE NEXT LEVEL", font, color, pos)
    get_ready_surface = ecs_world.component_for_entity(component_type=CSurface, entity=get_ready_text_entity)
    get_ready_surface.visible = False
    return get_ready_text_entity
