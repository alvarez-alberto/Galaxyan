import esper, pygame

from src.create.explosion_creator import create_explosion
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tag.c_tag_bullet_enemy import CTagBulletEnemy

def system_collision_bulletenemy_player(world: esper.World, player_entity: int, explosion_cfg:dict, sizew:int, sizeh:int):
    componentsbulletenemy = world.get_components(CSurface, CTransform, CTagBulletEnemy)

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_ast = world.component_for_entity(player_entity, CPlayerState)

    pl_rect:pygame.Rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    for bullet_enemy_entity, (c_s, c_t, c_tgb) in componentsbulletenemy:
        bullet_enemy_rect:pygame.Rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        
        if bullet_enemy_rect.colliderect(pl_rect):
            world.delete_entity(bullet_enemy_entity)
            create_explosion(world, pygame.Vector2(pl_rect.x, pl_rect.y), explosion_cfg)
            pl_t.pos = pygame.Vector2(sizew, sizeh)
            pl_ast.is_dead = True
            