import pygame

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_level_state import CLevelState, LevelState
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bulletenemy_player import system_collision_bulletenemy_player
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_level_state import system_level_state
from src.ecs.systems.s_player_spawn import system_player_spawn
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
from src.create.util_creator import crear_input_player, create_hi_score_text, create_max_score_text, create_score_value, create_stars_background, create_up_text
from src.create.enemy_creator import create_spawn, create_spawn_enemy_bullet
from src.create.play_creator import create_bullet, create_game_start_text, create_paused_text, create_player
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator

class ScenePlay(Scene):
    
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)

        self.level_01_cfg = ServiceLocator.configs_service.load_config("assets/cfg/level_01.json")
        self.enemies_cfg = ServiceLocator.configs_service.load_config("assets/cfg/enemies.json")
        self.bullets_cfg = ServiceLocator.configs_service.load_config("assets/cfg/bullets.json")
        self.explosions_cfg = ServiceLocator.configs_service.load_config("assets/cfg/explosions.json")
        self.player_cfg = ServiceLocator.configs_service.load_config("assets/cfg/player.json")

        self.invert = False
        self.delete_bullet_player = False
        self.sp_bullet_entity = 0

    def do_create(self):
        
        create_up_text(self.ecs_world)
        create_hi_score_text(self.ecs_world)
        create_max_score_text(self.ecs_world)
        create_score_value(self.ecs_world)
        create_stars_background(self.ecs_world)
        self.sp_bullet_entity = create_spawn_enemy_bullet(self.ecs_world, self.bullets_cfg["enemy"])
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st, self.pl_input_v = create_player(self.ecs_world)
        create_bullet(self.ecs_world,self.pl_entity,self.bullets_cfg)
        crear_input_player(self.ecs_world)
        self.game_start_text = create_game_start_text(self.ecs_world)
        self.pause_text = create_paused_text(self.ecs_world)

        self.pause_surface = self.ecs_world.component_for_entity(component_type=CSurface, entity=self.pause_text)
        self.pause_blink = self.ecs_world.component_for_entity(component_type=CBlink,entity=self.pause_text)

        ServiceLocator.sounds_service.play(self.level_01_cfg["game_start_sound"])

        level_entity = self.ecs_world.create_entity()
        self.c_level_state = CLevelState(self.game_start_text)
        self.ecs_world.add_component(level_entity, self.c_level_state)

    def do_update(self, delta_time: float,screen:pygame.Surface):

        system_level_state(self.ecs_world, self.c_level_state,self.level_01_cfg, delta_time, self.pl_entity)
        if self.c_level_state.state == LevelState.PLAY:
            system_movement(self.ecs_world,delta_time) 
            system_screen_player(self.ecs_world,screen)
            self.delete_bullet_player = system_screen_bullet(self.ecs_world,screen,self.pl_entity,self.bullets_cfg, self.delete_bullet_player, self.pl_entity, self.bullets_cfg)
            system_enemy_spawner(self.ecs_world, self.enemies_cfg, delta_time)
            self.invert = system_enemy_screen_bounce(self.ecs_world, self.enemies_cfg, self.invert)
            system_enemy_movement(self.ecs_world, delta_time, self.invert)
            system_enemy_shoot(self.ecs_world, self.bullets_cfg["enemy"], self.sp_bullet_entity, self.pl_entity, delta_time)
            system_enemy_shoot_movement(self.ecs_world, delta_time)
            self.delete_bullet_player = system_collision_bullet_enemy(self.ecs_world, self.explosions_cfg["enemy"], self.delete_bullet_player)
            system_collision_bulletenemy_player(self.ecs_world, self.pl_entity, self.explosions_cfg["player"], -100, -100)
            system_explosion_state(self.ecs_world)
            system_animation(self.ecs_world, delta_time)
            system_screen_limit_enemy_bullet(self.ecs_world, self.screen_rect, self.sp_bullet_entity)
            system_player_spawn(self.ecs_world, self.player_cfg["pos"]["x"], self.player_cfg["pos"]["y"], delta_time)
        
        system_starfield(self.ecs_world, delta_time)
        system_blink(self.ecs_world, delta_time)
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
                if self.c_level_state.state == LevelState.PLAY:
                    self.c_level_state.state = LevelState.PAUSED
                    self.pause_surface.visible = True
                    self.pause_blink.active = True
                    ServiceLocator.sounds_service.play(self.level_01_cfg["game_pause_sound"])                    
                elif self.c_level_state.state == LevelState.PAUSED:
                    self.c_level_state.state = LevelState.PLAY
                    self.pause_surface.visible = False
                    self.pause_blink.active = False

             