from sprites.shell import *
from settings import *
import pygame as pg
from timer import Timer
from pygame.sprite import AbstractGroup
from .prefabs import AimingPoint

# ------------------ULTIMATE--------------------------


class IUltimate:
    instance = None
    prefab = None

    def __init__(self, group, particle_group):
        self.group = group
        self.particle_group = particle_group
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }

    def Select(self, player_instance, *args, **kwargs):
        """Select ultimate"""

    def Use(self, player_instance, *args, **kwargs):
        """Use ultimate by controller event"""

    def __use(self, player_instance, *args, **kwargs):
        """main calling use function"""

    @property
    def isExecute(self):
        now = Timer.get_ticks()
        if now - self.updatingTime['last'] > self.updatingTime['cooldawn']:
            self.updatingTime['last'] = now
            return True
        return False

    @property
    def GerCooldawnDelta(self):
        return Timer.get_ticks() - (self.updatingTime['last'] + self.updatingTime['cooldawn'])


# ----------------------EFFECTS---------------------------

class IEffects(IUltimate):
    instance: object = None
    prefab = None
    duration: int = None


class Striker(IUltimate):
    instance: AimingPoint = None
    prefab = AimingPoint

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.image = pg.image.load(
            IMAGES+"\\game_objects\\strike_point.png").convert_alpha()
        self.label_image = pg.image.load(
            IMAGES+"\\menu\\labels\\strike_point.png").convert_alpha()
        self.updatingTime = {
            'last': 0,
            'cooldawn': 6000
        }

    def Select(self, player_instance, *args, **kwargs):
        return super().Select(player_instance, *args, **kwargs)

    def Use(self, player_instance, *args, **kwargs):
        if self.isExecute:
            self.__use(player_instance, *args, **kwargs)

        return super().Use(player_instance, *args, **kwargs)

    def __use(self, player_instance, *args, **kwargs):
        """Some action"""
        return super().__use(player_instance, *args, **kwargs)
