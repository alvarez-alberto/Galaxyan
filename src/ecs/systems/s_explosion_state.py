import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explosion_state import CExplosionState, ExplosionState
from src.ecs.components.c_velocity import CVelocity

def system_explosion_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CExplosionState)

    for explotion_entity, (c_v, c_a, c_pst) in components:
        if c_pst.state == ExplosionState.IDLE:
            _do_explode_state(c_a, world, explotion_entity)

def _do_explode_state(c_a:CAnimation, world: esper.World, explotion_entity:int):
    _set_animation(c_a, 0)

    if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
        world.delete_entity(explotion_entity)

def _set_animation(c_a:CAnimation, num_anim:int):
    if c_a.curr_anim == num_anim:
        return
    
    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start