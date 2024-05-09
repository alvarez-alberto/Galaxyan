import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tag.c_tag_bullet_enemy import CTagBulletEnemy

def system_enemy_shoot_movement(world:esper.World, delta_time:float):
    components = world.get_components(CTransform, CVelocity, CTagBulletEnemy)

    c_t:CTransform
    c_v:CVelocity

    for entity, (c_t, c_v, c_tbe) in components:
        c_t.pos.y += c_v.vel.y * delta_time