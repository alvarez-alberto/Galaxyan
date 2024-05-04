
import pygame
from src.create.menu_creator import create_start_game_text, create_title
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene
from src.create import prefab_creator

class SceneMenu(Scene):
    def do_create(self): 
        create_title(self.ecs_world)
        create_start_game_text(self.ecs_world)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action, CInputCommand("START", pygame.K_z))

    def do_action(self, action: CInputCommand) -> None:
        if action.name == "START" and action.phase == CommandPhase.START:
            self.switch_scene("PLAY_SCENE")

    def do_update(self, delta_time: float):
        pass
