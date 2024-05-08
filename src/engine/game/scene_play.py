import json, pygame

from src.create.play_creator import create_player
from src.create.enemy_creator import create_spawn
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_screen_bounce import system_enemy_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.engine.scenes.scene import Scene

class ScenePlay(Scene):
    
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        self.invert = False

    def do_create(self):
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st = create_player(self.ecs_world)
        create_spawn(self.ecs_world, self.level_01_cfg["enemy_spawn_events"])

    def do_update(self, delta_time: float):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, delta_time)
        self.invert= system_enemy_screen_bounce(self.ecs_world, self.enemies_cfg, self.invert)
        system_enemy_movement(self.ecs_world, delta_time, self.invert)
        system_animation(self.ecs_world, delta_time)
    
    def do_action(self, action: CInputCommand) -> None:
        pass
