
import json
import pygame
from src.create.play_creator import create_bullet, create_player
from src.create.util_creator import crear_input_player, create_stars_background
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_starfield import system_starfield
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.systems.s_fire_bullet import system_fire_bullet
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator

class ScenePlay(Scene):
    
    def do_create(self):
        with open("assets/cfg/bullets.json", encoding="utf-8") as bullet_config:
            self.bullet_cfg = json.load(bullet_config)
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st, self.pl_input_v = create_player(self.ecs_world)
        create_bullet(self.ecs_world,self.pl_entity,self.bullet_cfg)
        crear_input_player(self.ecs_world)
        create_stars_background(self.ecs_world)

    def do_update(self, delta_time: float,screen:pygame.Surface):
        system_movement(self.ecs_world,delta_time) 
        system_screen_player(self.ecs_world,screen,self.bullet_cfg["player"]["size"])
        system_screen_bullet(self.ecs_world,screen,self.pl_entity,self.bullet_cfg)
        
        system_starfield(self.ecs_world, delta_time)
        system_blink(self.ecs_world, delta_time)
    
    def do_action(self, action: CInputCommand) -> None:   
        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x -= self.pl_input_v
                for bullet_entity, _ in self.ecs_world.get_component(CTagBullet):
                    bullet_state = self.ecs_world.component_for_entity(bullet_entity, CBulletState)
                    if bullet_state.in_cannon:
                        bullet_vel = self.ecs_world.component_for_entity(bullet_entity, CVelocity)
                        bullet_vel.vel.x -= self.pl_input_v
            elif action.phase == CommandPhase.END:
                self.pl_v.vel.x += self.pl_input_v
                for bullet_entity, _ in self.ecs_world.get_component(CTagBullet):
                    bullet_state = self.ecs_world.component_for_entity(bullet_entity, CBulletState)
                    if bullet_state.in_cannon:
                        bullet_vel = self.ecs_world.component_for_entity(bullet_entity, CVelocity)
                        bullet_vel.vel.x += self.pl_input_v

        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x += self.pl_input_v
                for bullet_entity, _ in self.ecs_world.get_component(CTagBullet):
                    bullet_state = self.ecs_world.component_for_entity(bullet_entity, CBulletState)
                    if bullet_state.in_cannon:
                        bullet_vel = self.ecs_world.component_for_entity(bullet_entity, CVelocity)
                        bullet_vel.vel.x += self.pl_input_v
            elif action.phase == CommandPhase.END:
                self.pl_v.vel.x -= self.pl_input_v
                for bullet_entity, _ in self.ecs_world.get_component(CTagBullet):
                    bullet_state = self.ecs_world.component_for_entity(bullet_entity, CBulletState)
                    if bullet_state.in_cannon:
                        bullet_vel = self.ecs_world.component_for_entity(bullet_entity, CVelocity)
                        bullet_vel.vel.x -= self.pl_input_v

        if action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START: 
                ServiceLocator.sounds_service.play(self.bullet_cfg["player"]["sound"])        
                system_fire_bullet(self.ecs_world,self.bullet_cfg["player"]["velocity"])
                for bullet_entity, _ in self.ecs_world.get_component(CTagBullet):
                    bullet_state = self.ecs_world.component_for_entity(bullet_entity, CBulletState)
                    bullet_state.in_cannon = False
           