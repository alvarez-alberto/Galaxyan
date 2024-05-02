
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tag.c_tag_explosion import CTagExplosion

def system_explosion(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)

    c_a:CAnimation
    c_t_e:CTagExplosion
    for explosion , (c_a,c_t_e) in components:
        if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
            world.delete_entity(explosion)