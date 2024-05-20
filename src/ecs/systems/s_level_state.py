import esper
from src.create.enemy_creator import create_spawn
from src.create.play_creator import create_game_over_text
from src.create.util_creator import create_level_count
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemySpawnEvent
from src.ecs.components.c_level_state import CLevelState, LevelState
from src.ecs.components.c_level_text import CLevelText
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_level_state(ecs_world:esper.World, c_level_state:CLevelState, level_01_config:dict, delta_time:float, player_entity:int, level_complete_entity:int, get_ready_entity:int, level_count_entity:int):
    pl_ast = ecs_world.component_for_entity(player_entity, CPlayerState)
    
    if c_level_state.state == LevelState.START:
        c_level_state.state_time += delta_time
        if c_level_state.state_time > c_level_state.time_game_start:
            create_spawn(ecs_world, level_01_config["enemy_spawn_events"])
            c_level_state.state = LevelState.PLAY
            ecs_world.delete_entity(c_level_state.game_start_text)
            c_level_state.state_time = 0.0
            

    if pl_ast.is_dead and pl_ast.lives == 0 and c_level_state.state != LevelState.GAMEOVER and c_level_state.state != LevelState.START:
        c_level_state.state_time += delta_time
        if c_level_state.state_time > c_level_state.time_game_start:
            c_level_state.state = LevelState.GAMEOVER
            pl_ast.lives = 3
            c_level_state.state_time = 0.0
            create_game_over_text(ecs_world)
            ServiceLocator.sounds_service.play(level_01_config["game_over_sound"])

    if c_level_state.state == LevelState.NEXT_LEVEL:
        level_complete_surface = ecs_world.component_for_entity(component_type=CSurface, entity=level_complete_entity)
        get_ready_surface = ecs_world.component_for_entity(component_type=CSurface, entity=get_ready_entity)
        level_complete_surface.visible = True
        get_ready_surface.visible = True

        c_level_state.state_time += delta_time

        if c_level_state.state_time > level_01_config["time_to_next_level"]:
            componentspawnerenemy = ecs_world.get_component(CEnemySpawner)

            for entity, c_enemyspw in componentspawnerenemy:
                ecs_world.delete_entity(entity)
                
            create_spawn(ecs_world, level_01_config["enemy_spawn_events"])
            c_level_state.state = LevelState.PLAY
            c_level_state.state_time = 0.0
            level_complete_surface.visible = False
            get_ready_surface.visible = False

            surface_level_count = ecs_world.component_for_entity(level_count_entity, CSurface)
            level_text = ecs_world.component_for_entity(level_count_entity, CLevelText)
            surface_level_count.surf = CSurface.from_text(str(level_text.level).zfill(2), level_text.font, level_text.color).surf
            c_level_state.state_time = 0.0
