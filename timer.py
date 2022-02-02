import pygame as pg


class Timer:
    # instance = None
    ticks = 0

    def __init__(self):
        self.timer_update_event = pg.USEREVENT+1
        pg.time.set_timer(self.timer_update_event, 1)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Timer, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def update(*args, **kwargs):
        Timer.ticks += 1

    @staticmethod
    def reset(*args, **kwargs):
        Timer.ticks = 0

    @staticmethod
    def get_ticks(*args, **kwargs):
        return Timer.ticks

    @staticmethod
    def __str__(*args):
        return str(Timer.ticks)
