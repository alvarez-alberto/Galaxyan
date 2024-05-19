import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface


def system_blink(ecs_world:esper.World, delta_time:float):
    components = ecs_world.get_components(CSurface, CBlink)

    c_s: CSurface
    c_b: CBlink
  
    for entity, (c_s, c_b) in components:

        if not c_b.active:
            continue

        c_b.current_time += delta_time
        if c_b.current_time >= c_b.blink_interval:
            c_b.current_time = 0
            c_s.visible = not c_s.visible
        
