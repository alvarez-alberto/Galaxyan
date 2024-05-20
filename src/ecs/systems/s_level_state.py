import esper
from src.create.enemy_creator import create_spawn
from src.create.play_creator import create_game_over_text
from src.ecs.components.c_level_state import CLevelState, LevelState
from src.ecs.components.c_player_state import CPlayerState


def system_level_state(ecs_world:esper.World, c_level_state:CLevelState, level_01_config:dict, delta_time:float, player_entity:int):
    pl_ast = ecs_world.component_for_entity(player_entity, CPlayerState)
    
    if c_level_state.state == LevelState.START:
        c_level_state.state_time += delta_time
        if c_level_state.state_time > c_level_state.time_game_start:
            create_spawn(ecs_world, level_01_config["enemy_spawn_events"])
            c_level_state.state = LevelState.PLAY
            ecs_world.delete_entity(c_level_state.game_start_text)
            

    print(f"{c_level_state.state_time} {c_level_state.state}")
    if pl_ast.is_dead and pl_ast.lives == 0 and c_level_state.state != LevelState.GAMEOVER and c_level_state.state != LevelState.START:
        c_level_state.state = LevelState.GAMEOVER
        pl_ast.lives = 3
        c_level_state.state_time = 0.0
        create_game_over_text(ecs_world)

    
