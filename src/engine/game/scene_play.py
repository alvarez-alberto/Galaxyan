import json, pygame

from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_starfield import system_starfield
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.systems.s_fire_bullet import system_fire_bullet
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_screen_bounce import system_enemy_screen_bounce
from src.ecs.systems.s_enemy_shoot import system_enemy_shoot
from src.ecs.systems.s_enemy_shoot_movement import system_enemy_shoot_movement
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_screen_limit_enemy_bullet import system_screen_limit_enemy_bullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_bullet_state import CBulletState
from src.create.util_creator import crear_input_player, create_stars_background
from src.create.enemy_creator import create_spawn, create_spawn_enemy_bullet
from src.create.play_creator import create_bullet, create_player
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator

class ScenePlay(Scene):
    
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/bullets.json") as bullets_file:
            self.bullets_cfg = json.load(bullets_file)

        self.invert = False
        self.is_paused = False
        self.sp_bullet_entity = 0

    def do_create(self):
        create_stars_background(self.ecs_world)
        create_spawn(self.ecs_world, self.level_01_cfg["enemy_spawn_events"])
        self.sp_bullet_entity = create_spawn_enemy_bullet(self.ecs_world, self.bullets_cfg["enemy"])
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st, self.pl_input_v = create_player(self.ecs_world)
        create_bullet(self.ecs_world,self.pl_entity,self.bullets_cfg)
        crear_input_player(self.ecs_world)

    def do_update(self, delta_time: float,screen:pygame.Surface):
        if self.is_paused == False:
            system_movement(self.ecs_world,delta_time) 
            system_screen_player(self.ecs_world,screen)
            system_screen_bullet(self.ecs_world,screen,self.pl_entity,self.bullets_cfg)
            
            system_starfield(self.ecs_world, delta_time)
            system_blink(self.ecs_world, delta_time)
            
            system_enemy_spawner(self.ecs_world, self.enemies_cfg, delta_time)
            self.invert = system_enemy_screen_bounce(self.ecs_world, self.enemies_cfg, self.invert)
            system_enemy_movement(self.ecs_world, delta_time, self.invert)
            system_enemy_shoot(self.ecs_world, self.bullets_cfg["enemy"], self.sp_bullet_entity, delta_time)
            system_enemy_shoot_movement(self.ecs_world, delta_time)
            system_animation(self.ecs_world, delta_time)
            system_screen_limit_enemy_bullet(self.ecs_world, self.screen_rect, self.sp_bullet_entity)
        
        self.ecs_world._clear_dead_entities()
    
    def do_action(self, action: CInputCommand) -> None:   
        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x -= self.pl_input_v
                
            elif action.phase == CommandPhase.END:
                self.pl_v.vel.x += self.pl_input_v
                
        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x += self.pl_input_v
                
            elif action.phase == CommandPhase.END:
                self.pl_v.vel.x -= self.pl_input_v
                

        if action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START: 
                ServiceLocator.sounds_service.play(self.bullets_cfg["player"]["sound"])        
                system_fire_bullet(self.ecs_world,self.bullets_cfg["player"]["velocity"])
              

        if action.name == "PLAYER_PAUSE":
            if action.phase == CommandPhase.START:                
                self.is_paused = not self.is_paused   

    def do_draw_score(self, font ,screen, window , score:int):
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = (window["size"]["w"], 0)
        screen.blit(text, text_rect)                   