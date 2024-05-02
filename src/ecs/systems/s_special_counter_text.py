import pygame
import esper
from src.ecs.components.c_special_count import CSpecialCount
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator

def system_special_counter_text(world:esper.World, delta_time:float, bullet_special_info:dict):
    components = world.get_components(CSpecialCount, CSurface)
    c_s_c:CSpecialCount
    c_s:CSurface
    for _, (c_s_c, c_s) in components:
        if not c_s_c.ready:
            color = pygame.Color(255, 0, 0)
            c_s_c.curr_time += delta_time
            if c_s_c.curr_time > c_s_c.time:
                c_s_c.curr_time = c_s_c.time
                c_s_c.ready = True    
        else:
            color = pygame.Color(0, 255, 0)
        font = ServiceLocator.fonts_service.get(bullet_special_info["font"],bullet_special_info["size"])
        text = str(round((c_s_c.curr_time / c_s_c.time)* 100) ) + "%"
        c_s.surf = font.render(text, True, color)
        c_s.area = c_s.surf.get_rect()