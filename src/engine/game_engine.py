import asyncio
import json
import os
import pygame
import esper
from src.create.prefab_creator import crear_cuadrado, crear_input_player, crear_spawn_enemigos, create_bullet, create_bullet_special, create_description_text, create_paused_text, create_player_square, create_special_bullet_counter, create_special_bullet_title, create_title_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_special_count import CSpecialCount
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_hunter_state import sytem_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_enemy import system_screen_enemy
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_special_counter_text import system_special_counter_text 

class GameEngine:

    ENEMIES_CONFIG = "enemies.json"
    LEVEL_CONFIG = "level_01.json"
    WINDOW_CONFIG = "window.json"
    CONFIG_PATH = "assets/cfg"
    PLAYER_CONFIG = "player.json"
    BULLET_CONFIG = "bullet.json"
    EXPLOSION_CONFIG = "explosion.json"
    INTERFACE_CONFIG = "interface.json"

    def __init__(self) -> None:
        
        pygame.init()
        
        self.files_json_config()
        pygame.display.set_caption(self.window_cfg["title"])

        size_screen = self.window_cfg["size"]
        width = size_screen["w"]
        height = size_screen["h"]

        self.screen = pygame.display.set_mode(
            (width, height),
            0
        )

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.ecs_world = esper.World()
        self.paused = False


    def files_json_config(self):
        with open(os.path.join(self.CONFIG_PATH, self.WINDOW_CONFIG), encoding="utf-8") as window_config:
            self.window_cfg = json.load(window_config)
            
        with open(os.path.join(self.CONFIG_PATH, self.ENEMIES_CONFIG)) as enemies_config:
            self.enemies_cfg = json.load(enemies_config)
            
        with open(os.path.join(self.CONFIG_PATH, self.LEVEL_CONFIG)) as level_config:
            self.level_cfg = json.load(level_config)

        with open(os.path.join(self.CONFIG_PATH, self.PLAYER_CONFIG)) as player_config:
            self.player_cfg = json.load(player_config)

        with open(os.path.join(self.CONFIG_PATH, self.BULLET_CONFIG)) as bullet_config:
            self.bullet_config = json.load(bullet_config)
            self.bullet_cfg = self.bullet_config["bullet"]
            self.bullet_special_cfg = self.bullet_config["bullet_special"]
        
        with open(os.path.join(self.CONFIG_PATH, self.EXPLOSION_CONFIG)) as explosion_config:
            self.explosion_cfg = json.load(explosion_config)

        with open(os.path.join(self.CONFIG_PATH, self.INTERFACE_CONFIG)) as interface_config:
            self.interface_cfg = json.load(interface_config)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg, self.level_cfg["player_spawn"])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        crear_spawn_enemigos(self.ecs_world, self.level_cfg)
        crear_input_player(self.ecs_world)
        create_title_text(self.ecs_world, self.interface_cfg["title"])
        create_description_text(self.ecs_world, self.interface_cfg["description"])
        create_special_bullet_title(self.ecs_world, self.interface_cfg["bullet_special"])
        special_counter_entity = create_special_bullet_counter(self.ecs_world, self.interface_cfg["bullet_special"], self.bullet_special_cfg["special_time"])
        self._special_counter = self.ecs_world.component_for_entity(special_counter_entity, CSpecialCount)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):

        if not self.paused:
            system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
            system_movement(world=self.ecs_world, delta_time=self.delta_time)

            system_player_state(self.ecs_world)
            sytem_hunter_state(self.ecs_world, self._player_entity, self.enemies_cfg["Hunter"])

            system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg )
            system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_cfg , self.explosion_cfg)

            system_animation(self.ecs_world, self.delta_time)

            system_screen_bullet(self.ecs_world, self.screen)
            system_screen_enemy(self.ecs_world, self.screen)
            system_screen_player(self.ecs_world, self.screen)

            system_explosion(self.ecs_world)
            system_special_counter_text(self.ecs_world, self.delta_time, self.interface_cfg["bullet_special"])
            self.num_bullet = len(self.ecs_world.get_component(CTagBullet))
            self.ecs_world._clear_dead_entities()

    def _draw(self):
        screen_color = self.window_cfg["bg_color"]
        red = screen_color["r"]
        green = screen_color["g"]
        blue = screen_color["b"]

        self.screen.fill((red,green,blue))
        system_rendering(self.ecs_world,self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input:CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y += self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y -= self.player_cfg["input_velocity"]

        max_bullet_level = self.level_cfg["player_spawn"]["max_bullets"]
        if not self.paused and c_input.name == "PLAYER_FIRE" and max_bullet_level > self.num_bullet :
            if c_input.phase == CommandPhase.START:

                center_pos = self._player_c_s.area.copy()
                center_pos.topleft = self._player_c_t.pos
                start_pos = (
                    center_pos.centerx,center_pos.centery
                )
                create_bullet(self.ecs_world,c_input.mouse_pos,start_pos,self.bullet_cfg)

        if not self.paused and c_input.name == "PLAYER_SPECIAL_FIRE" and self.num_bullet > 0  and self._special_counter.ready :
            if c_input.phase == CommandPhase.START:
                create_bullet_special(self.ecs_world,self.bullet_special_cfg)
                self._special_counter.ready = False
                self._special_counter.curr_time = 0

        
        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.START:
                self.paused = not self.paused

                if self.paused:
                    self.paused_text = create_paused_text(self.ecs_world, self.interface_cfg["paused"])
                else:
                    self.ecs_world.delete_entity(self.paused_text)
