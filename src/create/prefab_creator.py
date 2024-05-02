
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_special_count import CSpecialCount
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.ecs.components.tag.c_tag_explosion import CTagExplosion
from src.ecs.components.tag.c_tag_player import CTagPlayer
from src.ecs.components.tag.c_tag_special_bullet import CTagSpecialBullet
from src.engine.service_locator import ServiceLocator

def crear_cuadrado(ecs_world:esper.World, size:pygame.Vector2, pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
        cuad_entity = ecs_world.create_entity()
        ecs_world.add_component(cuad_entity,
                                    CSurface(size, col))
        ecs_world.add_component(cuad_entity,
                                    CTransform(pos))
        ecs_world.add_component(cuad_entity,
                                    CVelocity(vel))
        return cuad_entity
        

def crear_spawn_enemigos(ecs_world:esper.World, level_config:dict):
        spawner_entity = ecs_world.create_entity()
        ecs_world.add_component(spawner_entity, CEnemySpawner(spawn_data=level_config["enemy_spawn_events"]))


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


def create_hunter(ecs_world:esper.World,pos:pygame.Vector2,velocity:pygame.Vector2, hunter_info: dict):
        hunter_surface = ServiceLocator.images_service.get(hunter_info["image"])
        hunter_entity = create_sprite(ecs_world, pos, velocity, hunter_surface)
        ecs_world.add_component(hunter_entity, CHunterState(pos))
        ecs_world.add_component(hunter_entity,CAnimation(hunter_info["animations"]))
        ecs_world.add_component(hunter_entity, CTagEnemy())


def create_player_square(ecs_world:esper.World, player_config:dict, player_level_config:dict) -> int:
        player_sprite = ServiceLocator.images_service.get(player_config["image"])
        size = player_sprite.get_size()
        size = (size[0] / player_config["animations"]["number_frames"], size[1])
        pos = pygame.Vector2(
                player_level_config["position"]["x"] - (size[0]/2),
                player_level_config["position"]["y"] - (size[1]/2)
        )
        vel = pygame.Vector2(0,0)

        player_entity = create_sprite(ecs_world,pos, vel, player_sprite)
        ecs_world.add_component(player_entity, CTagPlayer())
        ecs_world.add_component(player_entity, CAnimation(player_config["animations"]))
        ecs_world.add_component(player_entity, CPlayerState())

        return player_entity

def crear_input_player(ecs_world:esper.World):
        input_left = ecs_world.create_entity()
        input_right = ecs_world.create_entity()
        input_up = ecs_world.create_entity()
        input_down = ecs_world.create_entity()
        input_click_left = ecs_world.create_entity()
        input_key_p = ecs_world.create_entity()
        input_click_right = ecs_world.create_entity()

        ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
        ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
        ecs_world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
        ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
        ecs_world.add_component(input_click_left, CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))
        ecs_world.add_component(input_key_p, CInputCommand("PAUSE", pygame.K_p))
        ecs_world.add_component(input_click_right, CInputCommand("PLAYER_SPECIAL_FIRE", pygame.BUTTON_RIGHT))


def create_bullet(ecs_world: esper.World, mouse_pos: pygame.Vector2, start_pos: tuple, bullet_info: dict):
        bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
        direccion = pygame.Vector2(mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1])
        direccion.normalize_ip()
        vel = direccion * bullet_info["velocity"]   

        bullet_size = bullet_surface.get_rect().size
        pos = pygame.Vector2(
                start_pos[0] - (bullet_size[0]/2),
                 start_pos[1] - (bullet_size[1]/2)
                )
        bullet_entity = create_sprite(ecs_world,pos, vel, bullet_surface)
        ecs_world.add_component(bullet_entity, CTagBullet())
        ServiceLocator.sounds_service.play(bullet_info["sound"])

def create_bullet_special(ecs_world: esper.World, bullet_special_cf:dict):
        bullets = ecs_world.get_components(CTagBullet, CTransform)

        c_b:CTagBullet
        c_t:CTransform

        for bullet, (c_b,c_t) in bullets:
                if not ecs_world.has_component(bullet, CTagSpecialBullet):
                        ecs_world.delete_entity(bullet)
                        angulos_diagonales = [45, 135, 225, 315]
                        for i in range(0,4):
                                bullet_special_surface = ServiceLocator.images_service.get(bullet_special_cf["image"])
                                direccion = pygame.Vector2(0,1).rotate( angulos_diagonales[i])
                                vel = direccion * bullet_special_cf["velocity"]   
                                bullet_pos = c_t.pos.copy()
                                bullet_special_entity = create_sprite(ecs_world,bullet_pos, vel, bullet_special_surface)
                                ecs_world.add_component(bullet_special_entity, CTagSpecialBullet())
                                ecs_world.add_component(bullet_special_entity, CTagBullet())
                                ServiceLocator.sounds_service.play(bullet_special_cf["sound"])


def create_special_bullet_title(ecs_world: esper.World, bullet_interface_info:dict) -> int:
        text= bullet_interface_info["text_title"]
        font= ServiceLocator.fonts_service.get(bullet_interface_info["font"],bullet_interface_info["size"])
        color = pygame.Color(bullet_interface_info["color"]["r"],bullet_interface_info["color"]["g"],bullet_interface_info["color"]["b"])
        pos = pygame.Vector2(bullet_interface_info["position"]["x"],bullet_interface_info["position"]["y"])
        create_text(ecs_world, text, font, color, pos)
    
def create_special_bullet_counter(ecs_world: esper.World, bullet_interface_info:dict, special_time:float) -> int:
        text = bullet_interface_info["text"]
        font = ServiceLocator.fonts_service.get(bullet_interface_info["font"], bullet_interface_info["size"])
        color = pygame.Color(0, 255, 0)
        pos = pygame.Vector2(bullet_interface_info["position"]["x"],bullet_interface_info["position"]["y"]) + pygame.Vector2(0, 20)
        bullet_special_text_entity = create_text(ecs_world, text, font, color, pos)
        ecs_world.add_component(bullet_special_text_entity,CSpecialCount(special_time))
        return bullet_special_text_entity


def create_explosion(ecs_world:esper.World, pos:pygame.Vector2, explosion_info: dict):
        
        explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
        velocity = pygame.Vector2(0,0)

        explosion_entity = create_sprite(ecs_world, pos, velocity,explosion_surface)
        ecs_world.add_component(explosion_entity,CAnimation(explosion_info["animations"]))
        ecs_world.add_component(explosion_entity, CTagExplosion())
        ServiceLocator.sounds_service.play(explosion_info["sound"])

def create_paused_text(ecs_world:esper.World, paused_info:dict):
        text = paused_info["text"]
        font = ServiceLocator.fonts_service.get(paused_info["font"],paused_info["size"])
        color = pygame.Color(paused_info["color"]["r"],paused_info["color"]["g"],paused_info["color"]["b"])
        position = pygame.Vector2(paused_info["position"]["x"], paused_info["position"]["y"])
        return create_text(ecs_world, text, font, color, position)

def create_text(ecs_world:esper.World, text:str, font:pygame.font.Font, color:pygame.Color, position:pygame.Vector2):
        text_entity = ecs_world.create_entity()
        ecs_world.add_component(text_entity,CTransform(position))
        ecs_world.add_component(text_entity,CSurface.from_text(text, font, color))
        return text_entity


def create_title_text(ecs_world:esper.World, title_info:dict):
        text = title_info["text"]
        font = ServiceLocator.fonts_service.get(title_info["font"],title_info["size"])
        color = pygame.Color(title_info["color"]["r"],title_info["color"]["g"],title_info["color"]["b"])
        position = pygame.Vector2(title_info["position"]["x"], title_info["position"]["y"])
        return create_text(ecs_world, text, font, color, position)

def create_description_text(ecs_world:esper.World, title_info:dict):
        text = title_info["text"]
        font = ServiceLocator.fonts_service.get(title_info["font"],title_info["size"])
        color = pygame.Color(title_info["color"]["r"],title_info["color"]["g"],title_info["color"]["b"])
        position = pygame.Vector2(title_info["position"]["x"], title_info["position"]["y"])
        return create_text(ecs_world, text, font, color, position)