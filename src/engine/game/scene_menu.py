
import pygame
from src.create.menu_creator import create_start_game_text, create_title, create_card_slice
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_card_slice import system_card_slice
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_starfield import system_starfield
from src.engine.scenes.scene import Scene
from src.create.util_creator import create_hi_score_text, create_max_score_text, create_score_value, create_stars_background, create_up_text

class SceneMenu(Scene):
    def do_create(self): 
        title = create_title(self.ecs_world)
        start_text = create_start_game_text(self.ecs_world)
        up_text = create_up_text(self.ecs_world)
        hi_score_text = create_hi_score_text(self.ecs_world)
        max_score_text = create_max_score_text(self.ecs_world)
        score_value = create_score_value(self.ecs_world)

        create_card_slice(self.ecs_world, title)
        create_card_slice(self.ecs_world, start_text)
        create_card_slice(self.ecs_world, up_text)
        create_card_slice(self.ecs_world, hi_score_text)
        create_card_slice(self.ecs_world, max_score_text)
        create_card_slice(self.ecs_world, score_value)

        create_stars_background(self.ecs_world)

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action, CInputCommand("START", pygame.K_z))
        self.skip_intro = False

    def do_action(self, action: CInputCommand) -> None:
        if action.name == "START" and action.phase == CommandPhase.START:
            if self.skip_intro == True:
                self.switch_scene("PLAY_SCENE")
            else:
                self.skip_intro = True

    def do_update(self, delta_time: float,screen:pygame.Surface):

        system_starfield(self.ecs_world, delta_time)
        system_blink(self.ecs_world, delta_time)
        self.skip_intro = system_card_slice(self.ecs_world, self.skip_intro)
        system_movement(self.ecs_world, delta_time)
