import random
import esper
import pygame


from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
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


def crear_input_player(ecs_world:esper.World):
        input_left = ecs_world.create_entity()
        input_right = ecs_world.create_entity()      
        input_key_z = ecs_world.create_entity()       

        ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
        ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT)) 
        ecs_world.add_component(input_key_z, CInputCommand("PLAYER_FIRE", pygame.K_z))


def create_text(ecs_world:esper.World, text:str, font:pygame.font.Font, color:pygame.Color, position:pygame.Vector2):
        text_entity = ecs_world.create_entity()
        ecs_world.add_component(text_entity,CTransform(position))
        ecs_world.add_component(text_entity,CSurface.from_text(text, font, color))
        return text_entity







