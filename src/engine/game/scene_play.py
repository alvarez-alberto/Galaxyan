
from src.create.play_creator import create_player
from src.create.util_creator import create_stars_background
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_starfield import system_starfield
from src.engine.scenes.scene import Scene

class ScenePlay(Scene):
    
    def do_create(self):
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st = create_player(self.ecs_world)
        create_stars_background(self.ecs_world)

    def do_update(self, delta_time: float):
        system_starfield(self.ecs_world, delta_time)
        system_blink(self.ecs_world, delta_time)
    
    def do_action(self, action: CInputCommand) -> None:
        pass
