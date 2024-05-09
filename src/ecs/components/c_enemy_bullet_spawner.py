import pygame

class CEnemyBulletSpawner:
    def __init__(self, max_bullets:int, all_clean:bool, start:bool, start_time:float, time_attack_min:float, time_attack_max:float) -> None:
        self.max_bullets = max_bullets
        self.all_clean = all_clean
        self.start = start
        self.start_time = start_time
        self.current_time = 0.0
        self.time_attack_min = time_attack_min
        self.time_attack_max = time_attack_max
        self.time_next_attack = 0.0