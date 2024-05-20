
import random
import esper
import pygame

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_score_high_text import CHighScoreText
from src.ecs.components.c_score_text import CScoreText
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.ecs.components.tag.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator


def create_sprite(ecs_world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2, surface:pygame.Surface) -> int:
        sprite_entity = ecs_world.create_entity()
        ecs_world.add_component(sprite_entity, CTransform(pos))
        ecs_world.add_component(sprite_entity, CVelocity(vel)) 
        ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))
        return sprite_entity

def crear_enemigo(ecs_world:esper.World,new_enemy_info:dict,pos:pygame.Vector2):
        enemy_surface = ServiceLocator.images_service.get(new_enemy_info["image"])
        vel_min = new_enemy_info["velocity_min"]
        vel_max = new_enemy_info["velocity_max"]
        vel_range = vel_min + (random.random() * (vel_max - vel_min))
        velocity = pygame.Vector2(
              random.choice([-vel_range, vel_range]),
              random.choice([-vel_range, vel_range])
        )
        
        enemy_entity = create_sprite(ecs_world, pos, velocity, enemy_surface)
        ecs_world.add_component(enemy_entity, CTagEnemy())
        ServiceLocator.sounds_service.play(new_enemy_info["sound"])


def crear_input_player(ecs_world:esper.World):
        input_left = ecs_world.create_entity()
        input_right = ecs_world.create_entity()      
        input_key_z = ecs_world.create_entity() 
        input_key_p = ecs_world.create_entity()       

        ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
        ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT)) 
        ecs_world.add_component(input_key_z, CInputCommand("PLAYER_FIRE", pygame.K_z))
        ecs_world.add_component(input_key_p, CInputCommand("PLAYER_PAUSE", pygame.K_p))


def create_text(ecs_world:esper.World, text:str, font:pygame.font.Font, color:pygame.Color, position:pygame.Vector2):
        text_entity = ecs_world.create_entity()
        ecs_world.add_component(text_entity,CTransform(position))
        ecs_world.add_component(text_entity,CSurface.from_text(text, font, color))
        return text_entity


def create_stars_background(ecs_world: esper.World) -> None:
        
        starfield_cfg = ServiceLocator.configs_service.load_config("assets/cfg/starfield.json")

        star_colors = starfield_cfg["star_colors"]
        number_of_stars = starfield_cfg["number_of_stars"]
        vertical_speed_range = (starfield_cfg["vertical_speed"]["min"], starfield_cfg["vertical_speed"]["max"])
        blink_rate_range = (starfield_cfg["blink_rate"]["min"], starfield_cfg["blink_rate"]["max"])


        for _ in range(number_of_stars):
                star_entity = ecs_world.create_entity()

                random_color= random.choice(star_colors)
                color = pygame.color.Color(random_color["r"], random_color["g"], random_color["b"])

                vertical_speed = random.randint(vertical_speed_range[0], vertical_speed_range[1])
                vel = pygame.Vector2(0, vertical_speed)

                blink_rate = random.uniform(blink_rate_range[0], blink_rate_range[1])

                position = starfield_cfg["pos"] 
                x_range = random.randint(position["x_left"], position["x_right"])
                y_range = random.randint(position["y_top"], position["y_bottom"])
                pos = pygame.Vector2(x_range,y_range)

                size = starfield_cfg["size"]
                
                ecs_world.add_component(star_entity, CTagStar())
                ecs_world.add_component(star_entity, CSurface(pygame.Vector2(size["x"], size["y"]), color))
                ecs_world.add_component(star_entity, CTransform(pos))
                ecs_world.add_component(star_entity, CVelocity(vel))
                ecs_world.add_component(star_entity, CBlink(blink_rate))


def create_up_text(ecs_world:esper.World) -> int:
        interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
        menu_cfg = interface_cfg["menu"]
        color = pygame.color.Color(menu_cfg["title_text_color"]["r"],menu_cfg["title_text_color"]["g"],menu_cfg["title_text_color"]["b"])
        pos = pygame.Vector2(30,20)
        font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

        up_text_entity = create_text(ecs_world, "1UP", font, color, pos)
        ecs_world.add_component(up_text_entity, CVelocity(pygame.Vector2(0,0)))
        return up_text_entity

def create_hi_score_text(ecs_world:esper.World) -> int:
        interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
        menu_cfg = interface_cfg["menu"]
        color = pygame.color.Color(menu_cfg["title_text_color"]["r"],menu_cfg["title_text_color"]["g"],menu_cfg["title_text_color"]["b"])
        pos = pygame.Vector2(90,20)
        font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

        hi_score_entity = create_text(ecs_world, "HI-SCORE", font, color, pos)
        ecs_world.add_component(hi_score_entity, CVelocity(pygame.Vector2(0,0)))  
        return hi_score_entity  

def create_max_score_text(ecs_world:esper.World) -> int:
        interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
        menu_cfg = interface_cfg["menu"]
        color = pygame.color.Color(menu_cfg["high_score_color"]["r"],menu_cfg["high_score_color"]["g"],menu_cfg["high_score_color"]["b"])
        pos = pygame.Vector2(120,30)
        font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])

        #forma de cargar el max_score
        max_score = ServiceLocator.score_service.get_high_score_player()
        max_score_text = create_text(ecs_world, str(max_score), font, color, pos)
        ecs_world.add_component(max_score_text, CVelocity(pygame.Vector2(0,0)))
        ecs_world.add_component(max_score_text, CVelocity(pygame.Vector2(0,0)))
        ecs_world.add_component(max_score_text, CHighScoreText(max_score))
        return max_score_text  


def create_score_value(ecs_world:esper.World) -> int:
        interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
        menu_cfg = interface_cfg["menu"]
        color = pygame.color.Color(menu_cfg["normal_text_color"]["r"],menu_cfg["normal_text_color"]["g"],menu_cfg["normal_text_color"]["b"])
        pos = pygame.Vector2(40,30)
        font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])
        
        player_score = ServiceLocator.score_service.get_current_score_player()
        player_score_value = create_text(ecs_world, str(player_score), font, color, pos)
        ecs_world.add_component(player_score_value, CVelocity(pygame.Vector2(0,0)))
        ecs_world.add_component(player_score_value, CScoreText(player_score))
        return player_score_value 

def create_gameover_value(ecs_world:esper.World) -> int:
        interface_cfg = ServiceLocator.configs_service.load_config("assets/cfg/interface.json")
        menu_cfg = interface_cfg["menu"]
        color = pygame.color.Color(menu_cfg["normal_text_color"]["r"],menu_cfg["normal_text_color"]["g"],menu_cfg["normal_text_color"]["b"])
        pos = pygame.Vector2(40,30)
        font = ServiceLocator.fonts_service.get(menu_cfg["font"],menu_cfg["size"])
        
        player_score = ServiceLocator.score_service.get_current_score_player()
        player_score_value = create_text(ecs_world, str(player_score), font, color, pos)
        ecs_world.add_component(player_score_value, CVelocity(pygame.Vector2(0,0)))
        ecs_world.add_component(player_score_value, CScoreText(player_score))
        return player_score_value 