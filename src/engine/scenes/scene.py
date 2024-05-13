import pygame
import esper
import src.engine.game_engine
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_rendering import system_rendering


class Scene:
    def __init__(self, game_engine:'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self._game_engine:'src.engine.game_engine.GameEngine' = game_engine
        self.is_paused = False
        self.screen_rect = self._game_engine.screen.get_rect()

    def do_process_events(self, event:pygame.event):
        system_input_player(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time,screen):
        self.do_update(delta_time,screen)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()
    
    def switch_scene(self, new_scene_name:str):
        self._game_engine.switch_scene(new_scene_name)

    def do_create(self):
        pass

    def do_update(self, delta_time:float,screen:pygame.Surface):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def do_draw_score(self, font , screen, window ,score:int):
        pass

    def do_action(self, action:CInputCommand):
        pass
    
    def do_clean(self):
        self.ecs_world.clear_database()

    

