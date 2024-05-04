
from src.create.play_creator import create_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene

class ScenePlay(Scene):
    
    def do_create(self):
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st = create_player(self.ecs_world)

    def do_update(self, delta_time: float):
        pass
        
    
    def do_action(self, action: CInputCommand) -> None:
        pass
