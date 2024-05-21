import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_level_state import CLevelState, LevelState
from src.ecs.components.c_level_text import CLevelText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_enemy import CTagEnemy

def system_next_level(world:esper.World, c_level_state:CLevelState, level_count_entity:int):
    componentsenemy = world.get_components(CTagEnemy)

    if componentsenemy.__len__() <= 0 and c_level_state.state == LevelState.PLAY:
        c_level_state.state = LevelState.NEXT_LEVEL
        level_text = world.component_for_entity(level_count_entity, CLevelText)
        level_text.level += 1
