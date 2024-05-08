import esper, pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_enemy import CTagEnemy

def system_enemy_screen_bounce(world: esper.World, enemy_data:dict, invert: bool) -> bool:
    components = world.get_components(CTransform, CSurface, CTagEnemy)

    c_t:CTransform
    c_s:CSurface


    for entity, (c_t, c_s, c_e) in components:
        cuad_rect:pygame.Rect = CSurface.get_area_relative(c_s.area, c_t.pos)

        if cuad_rect.right >= enemy_data["limit_right"]:
            invert = True
            return invert
        
        if cuad_rect.left <= enemy_data["limit_left"]:
            invert = False
            return invert

    return invert
