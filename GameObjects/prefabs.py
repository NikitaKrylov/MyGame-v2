from animation import Animator
import pygame as pg
from pygame.sprite import AbstractGroup, Sprite
from timer import STimer, Timer
from pygame import Color, gfxdraw
# ----------Ultimate prefabs------------------


class AimingPoint(Sprite):
    """Hover point class used with some ultimates"""

    def __init__(self, image, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(center=pg.mouse.get_pos())

    def update(self, *args, **kwargs):
        pg.mouse.set_visible(False)
        joystick_hover_point = kwargs.get('joystick_hover_point')
        if joystick_hover_point:
            self.rect.centerx = joystick_hover_point.x
            self.rect.centery = joystick_hover_point.y
        else:
            self.rect.center = pg.mouse.get_pos()
        return super().update(*args, **kwargs)

    def draw(self, display):
        display.blit(self.image, self.rect)


# ----------Ultimate-effect prefabs------------------


class IEffect(Sprite):
    duration: int = None

    def __init__(self, duration=None, _effect_func=None, *groups: AbstractGroup):
        super().__init__(*groups)
        self.duration = duration if duration is not None else self.__class__.duration
        self._effect_func = _effect_func
        self.player_instance = None
        self.sTimer = STimer()
        self.finiteEvent = [self._revoke]

    def Use(self, player_instance, *args, **kwargs):
        self.player_instance = player_instance
        self._apply()
        self.sTimer.Start(self.duration, self.kill)

    def update(self, *args, **kwargs):
        self.sTimer.Update()

    def draw(self, display):
        pass

    def _revoke(self):
        pass

    def _apply(self):
        pass

    def AddfiniteEvent(self, function):
        self.finiteEvent.append(function)

    def kill(self):
        for f in self.finiteEvent:
            if f is not None:
                f()
        return super().kill()

    def ResetDurationTime(self):
        self.duration = self.__class__.duration


class InvisibleEffect(IEffect):
    duration = 3000

    def _apply(self):
        if self.player_instance is not None:
            self._effect_func(value=True)
        return super()._apply()

    def _revoke(self):
        if self.player_instance is not None:
            self._effect_func(value=False)
        return super()._revoke()

    def draw(self, display):
        gfxdraw.filled_circle(display,
                              self.player_instance.rect.centerx,
                              self.player_instance.rect.centery,
                              int(max(self.player_instance.rect.height,
                                  self.player_instance.rect.width)*0.6),
                              Color(30, 168, 247, 73))
        return super().draw(display)
