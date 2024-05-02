import pygame

class CEnemySpawner:
    def __init__(self, spawn_data:dict) -> None:
        self.time_spawn:float = 0.0

        self.spawn_events:list[EnemySpawnEvent] = []
        for event_data in spawn_data:
            time:float = event_data['time']
            enemy_type:str = event_data['enemy_type']
            position:pygame.Vector2 = pygame.Vector2(event_data['position']['x'], event_data['position']['y'])
            enemy_event = EnemySpawnEvent(time, enemy_type, position)
            self.spawn_events.append(enemy_event)


class EnemySpawnEvent:
    def __init__(self, time, enemy_type, position):
        self.time = time
        self.enemy_type = enemy_type
        self.position = position
        self.created = False
        
        