import pygame

class CEnemySpawner:
    def __init__(self, spawn_data:dict) -> None:
        self.time_spawn:float = 0.0

        self.spawn_events:list[EnemySpawnEvent] = []
        for event_data in spawn_data:
            time:float = event_data['time']
            enemy_type:str = event_data['enemy_type']
            position:pygame.Vector2 = pygame.Vector2(event_data['position']['x'], event_data['position']['y'])
            rows:int = event_data['rows']
            columns:int = event_data['columns']
            spacing_between_rows:int = event_data['spacing_between_rows']
            spacing_between_columns:int = event_data['spacing_between_columns']
            enemy_event = EnemySpawnEvent(time, enemy_type, position, rows, columns, spacing_between_rows, spacing_between_columns)
            self.spawn_events.append(enemy_event)


class EnemySpawnEvent:
    def __init__(self, time, enemy_type, position, rows, columns, spacing_between_rows, spacing_between_columns):
        self.time = time
        self.enemy_type = enemy_type
        self.position = position
        self.rows = rows
        self.columns = columns
        self.spacing_between_rows = spacing_between_rows
        self.spacing_between_columns = spacing_between_columns
        self.created = False
        
        