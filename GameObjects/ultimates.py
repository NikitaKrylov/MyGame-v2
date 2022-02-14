from sprites.shell import *
from settings import *
import pygame as pg
from timer import Timer
from pygame.sprite import AbstractGroup
from .prefabs import AimingPoint, InvisibleEffect

# ------------------ULTIMATE--------------------------


class IUltimate:
    instance = None
    prefab = None
    label_image = None

    def __init__(self, group, particle_group, BoolDeselectFubnc=None):
        self.BoolDeselectFubnc = BoolDeselectFubnc
        self.group = group
        self.particle_group = particle_group
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }

    def Select(self, isUsed, player_instance=None, *args, **kwargs):
        """Select ultimate"""

    def Use(self, player_instance, *args, **kwargs):
        """Use ultimate by controller event"""

    def _use(self, player_instance, *args, **kwargs):
        """main calling use function"""
        self.UpdateExecuteTime()

    @property
    def isExecute(self):
        now = Timer.get_ticks()
        if now - self.updatingTime['last'] > self.updatingTime['cooldawn']:
            return True
        return False
    
    def UpdateExecuteTime(self):
        self.updatingTime['last'] = Timer.get_ticks()

    @property
    def TimeDelta(self):
        delta = (self.updatingTime['last'] +
                 self.updatingTime['cooldawn']) - Timer.get_ticks()
        return delta if delta >= 0 else 0


class Striker(IUltimate):
    pointer = AimingPoint
    instance: AimingPoint = None
    prefab = Strike
    label_image = None

    def __init__(self, group, particle_group, BoolDeselectFubnc=None):
        super().__init__(group, particle_group, BoolDeselectFubnc)
        self.image = pg.image.load(
            IMAGES+"\\game_objects\\strike_point.png").convert_alpha()
        self.label_image = pg.image.load(
            IMAGES+"\\menu\\labels\\strike_point.png").convert_alpha()
        self.updatingTime = {
            'last': 0,
            'cooldawn': 6000
        }

    def Select(self, isUsed, player_instance=None, *args, **kwargs):
        if not isUsed and self.instance is not None:
            self.instance.kill()
            self.instance = None

        elif isUsed and self.instance is None:
            self.instance = self.__class__.pointer(self.image)
            self.particle_group.add(self.instance)

        return super().Select(isUsed, player_instance,  *args, **kwargs)

    def Use(self, player_instance=None, *args, **kwargs):
        if self.isExecute:
            self._use(player_instance, *args, **kwargs)

        return super().Use(player_instance=None, *args, **kwargs)

    def _use(self, player_instance=None, *args, **kwargs):
        image = pg.Surface((100, 100))
        image.fill((255, 90, 20))
        obj = self.prefab([image], self.instance.rect.center,
                          self.particle_group)
        self.group.add(obj)
        self.BoolDeselectFubnc()
        return super()._use(player_instance, *args, **kwargs)

# ----------------------EFFECTS---------------------------


class IEffectSender(IUltimate):
    instance: object = None
    prefab = None
    duration: int = None

    def Select(self, isUsed, player_instance=None, *args, **kwargs):
        if isUsed:
            self._use(player_instance, *args, **kwargs)

        return super().Select(isUsed, player_instance, *args, **kwargs)

    def Use(self, player_instance, *args, **kwargs):
        return super().Use(player_instance, *args, **kwargs)

    def _use(self, player_instance, *args, **kwargs):
        return super()._use(player_instance, *args, **kwargs)

    @property
    def TimeDelta(self):
        if self.instance is not None and self.instance.alive():
            return self.instance.sTimer.TimeDelta if hasattr(self.instance, "sTimer") else 0

        delta = (self.updatingTime['last'] +
                 self.updatingTime['cooldawn']) - Timer.get_ticks()
        return delta if delta >= 0 else 0


class InvisibleEffectSender(IEffectSender):
    instance: Sprite = None
    prefab = InvisibleEffect
    duration: int = 4000

    def __init__(self, group, particle_group, BoolDeselectFubnc=None):
        super().__init__(group, particle_group, BoolDeselectFubnc)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 6000
        }
        self.label_image = pg.image.load(
            IMAGES+"\\menu\\labels\\invisible_area.png").convert_alpha()

    def _use(self, player_instance, *args, **kwargs):
        if self.instance is not None and not self.instance.alive():
            self.instance = None

        if self.instance is None:
            self.instance = self.prefab(
                player_instance=player_instance,
                duration=self.duration, 
                _effect_func=player_instance.SetGodMode,)
            self.instance.AddfiniteEvent(self.BoolDeselectFubnc)
            self.instance.Use()
            player_instance.AddEffect(self.instance)
            self.BoolDeselectFubnc()

        return super()._use(player_instance, *args, **kwargs)
