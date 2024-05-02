

import asyncio
import json
import os
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.engine.game.scene_menu import SceneMenu
from src.engine.game.scene_play import ScenePlay
from src.engine.scenes.scene import Scene


class GameEngine:

    CONFIG_PATH = "assets/cfg"
    INTERFACE_CONFIG = "interface.json"
    WINDOW_CONFIG = "window.json"
    PLAYER_CONFIG = "player.json"

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

        self._scenes:dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = SceneMenu(self)
        self._scenes["PLAY_SCENE"] = ScenePlay(self)
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None

    def files_json_config(self):
        with open(os.path.join(self.CONFIG_PATH, self.WINDOW_CONFIG), encoding="utf-8") as window_config:
            self.window_cfg = json.load(window_config)
            
        with open(os.path.join(self.CONFIG_PATH, self.PLAYER_CONFIG), encoding="utf-8") as player_config:
            self.player_cfg = json.load(player_config)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._clean()

    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        screen_color = self.window_cfg["bg_color"]
        red = screen_color["r"]
        green = screen_color["g"]
        blue = screen_color["b"]

        self.screen.fill((red,green,blue))
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()