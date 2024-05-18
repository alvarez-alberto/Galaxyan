

class CCardSlice:
    def __init__(self, vel:float, start_pos:int, outside_pos:int) -> None:
        self.start_pos = start_pos
        self.outside_pos = outside_pos
        self.started = False
        self.vel = vel