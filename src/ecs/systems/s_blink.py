import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface


def system_blink(ecs_world:esper.World, delta_time:float):
    components = ecs_world.get_components(CSurface, CBlink)

    c_s: CSurface
    c_b: CBlink
  
    for star, (c_s, c_b) in components:

        c_b.current_time += delta_time
        if c_b.current_time >= c_b.blink_interval:
            c_b.current_time = 0
            c_b.active = not c_b.active

        if c_b.active:
            c_s.visible = True
        else:
            c_s.visible = False