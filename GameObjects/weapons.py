from sprites.shell import *
from settings import *
import pygame as pg
from timer import Timer
from pygame.sprite import AbstractGroup

# --------------------INTERFACE-----------------------


class IWeapon:
    prefab = None
    label_image = None

    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }
        self.group = group
        self.particle_group = particle_group
        self.images = []

    def Use(self, rect, *args, **kwargs):
        """Using weapon"""

    @property
    def isExecute(self):
        now = Timer.get_ticks()
        if now - self.updatingTime['last'] > self.updatingTime['cooldawn']:
            self.updatingTime['last'] = now
            return True
        return False

    @property
    def GetCooldawnDelta(self):
        delta = (self.updatingTime['last'] + self.updatingTime['cooldawn']) - Timer.get_ticks()
        return  delta if delta >= 0 else 0


# --------------------BASE-----------------------

class BaseWeapon(IWeapon):
    prefab = BaseShell
    label_image = None

    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        super().__init__(group, particle_group)
        self.images = []

    def Use(self, rect, *args, **kwargs):
        self.prefab(self.images, rect.center, self.particel_group, self.group)
        return super().Use(rect, *args, **kwargs)


# --------------------PLAYER-----------------------

class SingleRedGun(IWeapon):
    prefab = RedShell

    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        super().__init__(group, particle_group)
        self.images = [pg.image.load(
            IMAGES+'\shell\\red\\redshell'+str(i)+'.png').convert_alpha() for i in range(1, 2)]

    def Use(self, rect, *args, **kwargs):
        pos = rect.center if not kwargs.get('pos') else kwargs.get('pos')
        self.prefab(images=self.images, particle_group=self.particle_group, groups=[
                    self.group], **kwargs)
        return super().Use(rect, *args, **kwargs)


class BurnedLauncher(IWeapon):
    prefab = BurnedShell

    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        super().__init__(group, particle_group)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 300
        }
        self.images = [pg.image.load(
            IMAGES+'\shell\\orange\\orange.png').convert_alpha()]

    def Use(self, rect, *args, **kwargs):
        if self.isExecute:
            pos = [rect.centerx, rect.top + self.images[0].get_height()//1.5]
            self.prefab(self.images, pos, self.particle_group, self.group)
            return super().Use(rect, *args, **kwargs)


class LiteGun(IWeapon):
    prefab = FirstShell

    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        super().__init__(group, particle_group)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 100
        }
        self.images = [pg.image.load(
            IMAGES+'\shell\lite\shell1.png').convert_alpha()]
        self.label_image = pg.image.load(
            IMAGES+'\\menu\\labels\\lite.png').convert_alpha()

    def Use(self, rect, *args, **kwargs):
        if self.isExecute:
            pos = [rect.centerx, int(
                rect.top+self.images[0].get_rect().height//2)]
            self.prefab(self.images, pos, self.particle_group, self.group)
        return super().Use(rect, *args, **kwargs)


class RocketLauncher(IWeapon):
    prefab = Rocket

    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        super().__init__(group, particle_group)
        self.images = [pg.image.load(
            IMAGES+'\shell\\racket\\racket.png').convert_alpha()]
        self.updatingTime = {
            'last': 0,
            'cooldawn': 1000
        }

    def Use(self, rect, *args, **kwargs):
        if self.isExecute:
            self.prefab(self.images, rect.center,
                        self.particle_group, [self.group])
            return super().Use(rect, *args, **kwargs)


# --------------------ENEMY-----------------------
