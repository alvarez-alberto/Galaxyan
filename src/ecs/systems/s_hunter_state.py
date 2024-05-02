
import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def sytem_hunter_state(ecs_world:esper.World, player_entity:int, hunter_cnf:dict):
    components = ecs_world.get_components(CVelocity, CAnimation,CTransform, CHunterState)
    p_t = ecs_world.component_for_entity(player_entity, CTransform)

    c_v: CVelocity
    c_a: CAnimation
    c_t: CTransform
    c_hs: CHunterState 

    for _, (c_v,c_a,c_t,c_hs) in components:
        if c_hs.state == HunterState.IDLE:
            _do_idle_state(c_v,c_a,c_t,c_hs,hunter_cnf,p_t)
        elif c_hs.state == HunterState.CHASE:
            _do_chase_state(c_v,c_a,c_t,c_hs,hunter_cnf,p_t, c_hs.pos)
        elif c_hs.state == HunterState.RETURN:
            _do_return_state(c_v,c_a,c_t,c_hs,hunter_cnf,p_t, c_hs.pos)

def _do_idle_state(c_v:CVelocity, c_a:CAnimation,c_t:CTransform, c_hs:CHunterState,hunter_cnf:dict,p_t:CTransform):
    _set_animation(c_a,1)
    c_v.vel = pygame.Vector2(0,0)

    distance_start_chase = hunter_cnf["distance_start_chase"]
    go_to_chase = c_t.pos.distance_to(p_t.pos) < distance_start_chase 
    if go_to_chase:
        ServiceLocator.sounds_service.play(hunter_cnf["sound_chase"])
        c_hs.state = HunterState.CHASE


def _do_chase_state(c_v:CVelocity, c_a:CAnimation,c_t:CTransform, c_hs:CHunterState,
                    hunter_cnf:dict,p_t:CTransform, origen:pygame.Vector2):
    _set_animation(c_a,0)
    dir = (p_t.pos - c_t.pos).normalize()
    c_v.vel = dir * hunter_cnf["velocity_chase"]
    distance_start_return = hunter_cnf["distance_start_return"]
    go_to_return = distance_start_return < c_t.pos.distance_to(origen)
    if go_to_return:
        c_hs.state = HunterState.RETURN 

         
def _do_return_state(c_v:CVelocity, c_a:CAnimation,c_t:CTransform, c_hs:CHunterState,
                    hunter_cnf:dict,p_t:CTransform, origen:pygame.Vector2):
    _set_animation(c_a,0)

    dir = (origen - c_t.pos).normalize()
    c_v.vel = dir * hunter_cnf["velocity_return"]
    go_to_idle = origen.distance_to(c_t.pos) < 1
    if go_to_idle:
        c_hs.state = HunterState.IDLE 


def _set_animation(c_a:CAnimation, num_anim:int):
    if c_a.curr_anim == num_anim:
        return
    
    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start