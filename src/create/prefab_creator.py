
import random
import esper
import pygame


from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_enemy import CTagEnemy
from src.ecs.components.tag.c_tag_player import CTagPlayer
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


def create_player(world: esper.World, player_config:dict):
        surface = ServiceLocator.images_service.get(player_config["image"])
        pos = pygame.Vector2(player_config["spawn_point"]["x"],  
                                player_config["spawn_point"]["y"])
        vel = pygame.Vector2(0, 0)
        player_entity = create_sprite(world, pos, vel, surface)
        world.add_component(player_entity, CTagPlayer(player_config["input_speed"]))
        world.add_component(player_entity, CPlayerState(player_config["lives"]))
        player_tr = world.component_for_entity(player_entity, CTransform)
        player_v = world.component_for_entity(player_entity, CVelocity)
        player_tag = world.component_for_entity(player_entity, CTagPlayer)
        player_state = world.component_for_entity(player_entity, CPlayerState)
        return (player_entity, player_tr, player_v, player_tag, player_state)

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







