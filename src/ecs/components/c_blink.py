class CBlink:
    def __init__(self, blink_interval):
        self.active = True  # Comienza activo
        self.blink_interval = blink_interval
        self.current_time = 0
