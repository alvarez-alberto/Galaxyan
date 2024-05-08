import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_star import CTagStar


def system_starfield(ecs_world:esper.World, delta_time:float):
    components = ecs_world.get_components(CTransform, CVelocity, CTagStar)

    c_t: CTransform
    c_v: CVelocity
    c_ts: CTagStar

    for star, (c_t, c_v, c_ts) in components:
        c_t.pos += c_v.vel * delta_time
        if (c_t.pos.y > 240):
            c_t.pos.y = 0