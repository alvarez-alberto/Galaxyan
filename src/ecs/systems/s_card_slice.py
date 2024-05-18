import esper
from src.ecs.components.c_card_slice import CCardSlice
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_card_slice(ecs_world:esper.World):
    card_components = ecs_world.get_components(CCardSlice, CTransform, CVelocity)

    cc_s:CCardSlice
    c_t:CTransform
    c_v:CVelocity
    for card, (cc_s, c_t, c_v) in card_components:

        if cc_s.started:
            c_v.vel.y = cc_s.vel
            _outside(cc_s,c_t,c_v,ecs_world,card)
        else:
            cc_s.started = True
            c_t.pos.y = cc_s.start_pos


def _outside(cc_s:CCardSlice,c_t:CTransform, c_v:CVelocity, ecs_word:esper.World, card):

    if c_t.pos.y <= cc_s.outside_pos:
                c_t.pos.y = cc_s.outside_pos
                c_v.vel.y = 0
                ecs_word.remove_component(card, CCardSlice)

    
    