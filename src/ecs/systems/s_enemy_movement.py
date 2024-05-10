import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_enemy import CTagEnemy

def system_enemy_movement(world:esper.World, delta_time:float, invert: bool):
    components = world.get_components(CTransform, CVelocity, CTagEnemy)

    c_t:CTransform
    c_v:CVelocity

    for entity, (c_t, c_v, c_te) in components:
        if invert == False:
            c_t.pos.x += c_v.vel.x * delta_time
        else:
            c_t.pos.x += c_v.vel.x *-1 * delta_time
