import esper, pygame

from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_player import CTagPlayer
from src.ecs.components.c_level_state import CLevelState, LevelState

def system_player_spawn(world:esper.World, posx:int, posy:int, c_level_state:CLevelState, delta_time:float):    
    components = world.get_components(CTransform, CVelocity, CTagPlayer, CPlayerState)

    c_t:CTransform
    c_v:CVelocity

    for entity, (c_t, c_v, c_tgp, c_plst) in components:
        if c_plst.is_dead:
            c_plst.current_time += delta_time

            if c_plst.current_time > c_plst.time_spawn and c_level_state.state == LevelState.PLAY:
                c_plst.is_dead = False
                c_t.pos = pygame.Vector2(posx, posy)
                c_plst.current_time = 0.0
