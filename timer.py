import pygame as pg


class Timer:
    # instance = None
    ticks = 0

    def __init__(self):
        self.timer_update_event = pg.USEREVENT+1
        self.sprite_group_update_event = pg.USEREVENT+2
        
        self.FPSUpdate = 20
        
        pg.time.set_timer(self.sprite_group_update_event, self.FPSUpdate)
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


class STimer:
    def Start(self, rate: int, finite_func=None):
        self.rate = rate
        self.finite_func = finite_func
        self.finiteTime = Timer.get_ticks() + self.rate

    def Update(self, *args, **kwargs):
        if Timer.get_ticks() > self.finiteTime:
            if self.finite_func:
                self.finite_func()
            return True
        return False

    @property
    def TimeDelta(self):
        delta = self.finiteTime - Timer.get_ticks()
        return delta if delta > 0 else 0
