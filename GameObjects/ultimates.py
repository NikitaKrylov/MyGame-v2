from sprites.shell import *
from settings import *
import pygame as pg
from timer import Timer
from .prefabs import AimingPoint, InvisibleEffect, RageEffect

# ------------------ULTIMATE--------------------------


class IUltimate:
    instance = None
    prefab = None
    label_image = None

    def __init__(self, group, particle_group, BoolDeselectFunc=None):
        self.BoolDeselectFunc = BoolDeselectFunc
        self.group = group
        self.particle_group = particle_group
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }
        self.UpdateExecuteTime()

    def Select(self, isUsed, player_instance=None, *args, **kwargs):
        """Select ultimate"""

    def Use(self, player_instance, *args, **kwargs):
        """Use ultimate by controller event"""

    def _use(self, player_instance, *args, **kwargs):
        """main calling use function"""
        self.UpdateExecuteTime()
        self.BoolDeselectFunc()

    @property
    def isExecute(self):
        now = Timer.get_ticks()
        if now - self.updatingTime['last'] > self.updatingTime['cooldawn']:
            return True
        return False

    @property
    def isSelectable(self):
        return self.isExecute

    def UpdateExecuteTime(self):
        self.updatingTime['last'] = Timer.get_ticks()

    @property
    def TimeDelta(self):
        delta = (self.updatingTime['last'] +
                 self.updatingTime['cooldawn']) - Timer.get_ticks()

        return delta if delta >= 0 else 0


class Striker(IUltimate):
    pointer_prefab = AimingPoint
    pointer: AimingPoint = None
    prefab = Strike
    label_image = None

    def __init__(self, group, particle_group, BoolDeselectFunc=None):
        super().__init__(group, particle_group, BoolDeselectFunc)
        self.image = pg.image.load(
            IMAGES+"\\game_objects\\strike_point.png").convert_alpha()
        self.label_image = pg.image.load(
            IMAGES+"\\menu\\labels\\strike_point.png").convert_alpha()
        self.updatingTime['cooldawn'] = 6000

    def Select(self, isUsed, player_instance=None, *args, **kwargs):
        if self.isExecute:
            if not isUsed and self.pointer is not None:
                self.pointer.kill()
                self.pointer = None

            elif isUsed and self.pointer is None:
                self.pointer = self.__class__.pointer_prefab(self.image)
                self.particle_group.add(self.pointer)

        return super().Select(isUsed, player_instance,  *args, **kwargs)

    def Use(self, player_instance=None, *args, **kwargs):
        if self.isExecute:
            self._use(player_instance, *args, **kwargs)

        return super().Use(player_instance=None, *args, **kwargs)

    @property
    def isSelectable(self):
        return self.isExecute

    def _use(self, player_instance=None, *args, **kwargs):
        image = pg.Surface((100, 100))
        image.fill((255, 90, 20))
        obj = self.prefab([image], self.pointer.rect.center,
                          self.particle_group)
        self.group.add(obj)
        self.pointer.kill()
        self.pointer = None
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
        """create effect object, add effect to player
        or kill and set to None effect instance """
        if self.instance is not None and not self.instance.alive():
            self.instance = None

        if self.instance is None:
            self.instance = self.CreateEffect(player_instance)
            player_instance.AddEffect(self.instance)
        return super()._use(player_instance, *args, **kwargs)

    def CreateEffect(self, player_instance):
        pass

    @property
    def DeltaDuration(self):
        return self.instance.sTimer.TimeDelta if hasattr(self.instance, "sTimer") else 0

    @property
    def TimeDelta(self):
        if self.instance is not None and self.instance.alive():
            return self.DeltaDuration
        return super().TimeDelta


class InvisibleEffectSender(IEffectSender):
    instance: Sprite = None
    prefab = InvisibleEffect
    duration: int = 4000

    def __init__(self, group, particle_group, BoolDeselectFunc=None):
        super().__init__(group, particle_group, BoolDeselectFunc)
        self.updatingTime['cooldawn'] = 3000 + self.__class__.duration
        self.label_image = pg.image.load(
            IMAGES+"\\menu\\labels\\invisible_area.png").convert_alpha()

    def CreateEffect(self, player_instance):
        instance = self.prefab(
            player_instance=player_instance,
            duration=self.duration,
            _effect_func=player_instance.SetGodMode,)
        instance.AddfiniteEvent(self.BoolDeselectFunc)
        instance.Use()
        return instance


class RageEffectSender(IEffectSender):
    instance: Sprite = None
    prefab = RageEffect
    duration: int = 4000

    def CreateEffect(self, player_instance):
        instance = RageEffectSender.prefab(
            player_instance=player_instance,
            duration=RageEffect.duration,
            _effect_func=None)
        return instance
