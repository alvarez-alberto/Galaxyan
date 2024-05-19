import esper
from src.create.enemy_creator import create_spawn
from src.ecs.components.c_level_state import CLevelState, LevelState


def system_level_state(ecs_world:esper.World, c_level_state:CLevelState, level_01_config:dict, delta_time:float):
    
    if c_level_state.state == LevelState.START:
        c_level_state.state_time += delta_time
        if c_level_state.state_time > c_level_state.time_game_start:
            create_spawn(ecs_world, level_01_config["enemy_spawn_events"])
            c_level_state.state = LevelState.PLAY
            ecs_world.delete_entity(c_level_state.game_start_text)


