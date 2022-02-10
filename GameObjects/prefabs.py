import pygame as pg
from pygame.sprite import AbstractGroup, Sprite

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

    def __init__(self, _effect_func=None, *groups: AbstractGroup):
        super().__init__(*groups)
        self._effect_func = _effect_func
        self.duration = self.__class__.duration
        self.player_instance = None

    def Use(self, player_instance, *args, **kwargs):
        self.player_instance = player_instance
        self._apply()

    def update(self, *args, **kwargs):
        print("Im working")

    def _revoke(self):
        pass

    def _apply(self):
        pass

    def kill(self):
        self._revoke()
        return super().kill()

    def ResetDurationTime(self):
        self.duration = self.__class__.duration


class InvisibleEffect(IEffect):
    duration = 6000

    def _apply(self):
        if self.player_instance is not None:
            self._effect_func(value=True)
        return super()._apply()

    def _revoke(self):
        if self.player_instance is not None:
            self._effect_func(value=False)
        return super()._revoke()
