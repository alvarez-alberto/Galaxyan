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

    CONFIG_PATH = "assets/cfg"
    INTERFACE_CONFIG = "interface.json"
    STARFIELD_CONFIG = "starfield.json"
    WINDOW_CONFIG = "window.json"

    def __init__(self) -> None:
        
        pygame.init()
        
        self.files_json_config()
        pygame.display.set_caption(self.window_cfg["title"])

        size_screen = self.window_cfg["size"]
        width = size_screen["w"]
        height = size_screen["h"]

        self.screen = pygame.display.set_mode(
            (width, height),pygame.SCALED
        )
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.ecs_world = esper.World()

    def files_json_config(self):
        with open(os.path.join(self.CONFIG_PATH, self.WINDOW_CONFIG), encoding="utf-8") as window_config:
            self.window_cfg = json.load(window_config)
            
        with open(os.path.join(self.CONFIG_PATH, self.STARFIELD_CONFIG)) as starfield_config:
            self.starfield_cfg = json.load(starfield_config)
            
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
        pass

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        pass


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
        pass
