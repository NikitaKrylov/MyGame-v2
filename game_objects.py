from math import ceil
import pygame as pg
from pygame import surface
from animation import Animator, StaticMovement
# from sprites.shell import *
from pygame.sprite import Sprite, AbstractGroup
from sprites.shell import BaseShell, BurnedShell, FirstShell, RedEnemyShell, Rocket, RedShell, StarEnemyShell
from pygame.sprite import Group
from settings import IMAGES


def sign(value):
    return 1 if value > 0 else -1


class ObjectInterface(Sprite):
    def __init__(self, pos: list, image, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.direction = pg.Vector2(0, 1)

    def execute(self):
        pass

    def draw(self, display, *args, **kwargs):
        display.blit(self.image, self.rect)

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)


class AbstructHeal(ObjectInterface):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)

    def execute(self):
        return super().execute()

# -------------------------------------


class AbstaructWeapon:

    def __init__(self):
        self.__isExecute = True
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }

    def execute(self, *args, **kwargs):
        return

    @property
    def isExecute(self):
        now = pg.time.get_ticks()
        if now - self.updatingTime['last'] > self.updatingTime['cooldawn']:
            self.updatingTime['last'] = now
            return True
        return False


class AbstractUltimate(AbstaructWeapon):
    def __init__(self, group, particle_group):
        super().__init__()
        self.group = group
        self.particle_group = particle_group

    def select(self, isUsed, *args, **kwargs):
        pass

# -----------------------------------


class AimingPoint(Sprite):
    """Hover point class used with some ultimates"""

    def __init__(self, image, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(center=pg.mouse.get_pos())
        # self.movement = StaticMovement(pg.Vector2(0, 0))

    def update(self, *args, **kwargs):
        joystick_hover_point = kwargs.get('joystick_hover_point')
        if joystick_hover_point:
            self.rect.centerx = joystick_hover_point.x
            self.rect.centery = joystick_hover_point.y
        else:
            self.rect.center = pg.mouse.get_pos()
        return super().update(*args, **kwargs)

    def draw(self, display):
        display.blit(self.image, self.rect)


class Strike(BaseShell):
    _damage = 300
    _speed = 0

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.movement.direction = pg.Vector2(0, 0)

    def update(self, *args, **kwargs):
        self.animation.update(
            now=kwargs['now'], rate=200, frames_len=2, repeat=False, finiteFunction=self.kill)
        return super().update(*args, **kwargs)


# -----------------------------


class StrikeUltimate(AbstractUltimate):

    AimingPointInstance = None

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.image = pg.image.load(
            IMAGES+"\\game_objects\\strike_point.png").convert_alpha()
        self.updatingTime = {
            'last': 0,
            'cooldawn': 2300
        }

    def select(self, isUsed, *args, **kwargs):
        if not isUsed and self.AimingPointInstance != None:
            self.AimingPointInstance.kill()
            self.AimingPointInstance = None

        if isUsed and self.AimingPointInstance == None:
            _aimingPoint = AimingPoint(self.image)
            self.particle_group.add(_aimingPoint)
            self.AimingPointInstance = _aimingPoint

        return super().select(isUsed, *args, **kwargs)

    def execute(self, *args, **kwargs):
        if self.isExecute:
            image = pg.Surface((100, 100))
            image.fill((255, 90, 20))
            obj = Strike([image], self.AimingPointInstance.rect.center,
                         self.particle_group)
            self.group.add(obj)

# ------------------------------------------------------------------------


class AbstractGun(AbstaructWeapon):
    amo = BaseShell

    def __init__(self, group, particle_group):
        super().__init__()
        self.particle_group = particle_group
        self.group = group
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }

    def execute(self, *args, **kwargs):
        return super().execute()


class FirstGun(AbstractGun):
    amo = FirstShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.images = [pg.image.load(
            IMAGES+'\shell\lite\shell'+str(i)+'.png').convert_alpha() for i in range(1, 6)]

    def execute(self, rect, *args, **kwargs):
        pos = [rect.centerx, int(rect.top+self.images[0].get_rect().height//2)]
        self.group.add(self.amo(self.images, pos,
                       self.particle_group, [self.group]))
        return super().execute()


class SingleRedGun(AbstractGun):
    amo = RedShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 1700
        }
        self.images = [pg.image.load(
            IMAGES+'\shell\\red\\redshell'+str(i)+'.png').convert_alpha() for i in range(1, 2)]

    def execute(self, rect, *args, **kwargs):
        pos = rect.center if not kwargs.get('pos') else kwargs.get('pos')

        self.group.add(self.amo(
            images=self.images, particle_group=self.particle_group, groups=[self.group], **kwargs))
        return super().execute()


class DubleRedGun(SingleRedGun):
    amo = RedShell

    def execute(self, rect, *args, **kwargs):
        pos1 = [rect.left, rect.top+rect.height//2]
        pos2 = [rect.right, pos1[1]]
        self.group.add(self.amo(self.images, pos1,
                       self.particle_group))
        self.group.add(self.amo(self.images, pos2,
                       self.particle_group))


class StarGun(AbstractGun):
    amo = StarEnemyShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        # image = pg.Surface((15, 15))
        # image.fill('#71c0f2')
        # self.images = [image]
        self.images = [pg.image.load(
            IMAGES+'\shell\\star\\star1.png').convert_alpha()]
        self.updatingTime = {
            'last': 0,
            'cooldawn': 800
        }

    def execute(self, *args, **kwargs):
        self.group.add(self.amo(images=self.images,
                       particle_group=self.particle_group, **kwargs))


class SingleRedGunEnemy(SingleRedGun):
    amo = RedEnemyShell

    def execute(self, rect, *args, **kwargs):
        if self.isExecute:
            pos = [rect.centerx, rect.bottom]
            self.amo(self.images, pos, self.particle_group, self.group)


class DubleGunEnemy(DubleRedGun):
    amo = RedEnemyShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 1700
        }

    def execute(self, rect, *args, **kwargs):
        if self.isExecute:
            pos1 = [rect.left, rect.top+rect.height//2]
            pos2 = [rect.right, pos1[1]]
            self.group.add(self.amo(self.images, pos1,
                                    self.particle_group))
            self.group.add(self.amo(self.images, pos2,
                                    self.particle_group))
        return


class RocketLauncher(AbstractGun):
    amo = Rocket

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        # self.images = [pg.image.load(
        # IMAGES+'\shell\\racket\\racket'+str(i)+'.png').convert_alpha() for i in range(1, 7)]
        self.images = [pg.image.load(
            IMAGES+'\shell\\racket\\racket.png').convert_alpha()]
        self.updatingTime = {
            'last': 0,
            'cooldawn': 1000
        }

    def execute(self, rect, *args, **kwargs):
        if self.isExecute:
            self.group.add(self.amo(self.images, rect.center,
                                    self.particle_group, [self.group]))
            return super().execute()


class BurnedLauncher(AbstractGun):
    amo = BurnedShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 100
        }
        self.images = [pg.image.load(
            IMAGES+'\shell\\orange\\orange.png').convert_alpha()]

    def execute(self, rect, *args, **kwargs):
        if self.isExecute:
            pos = [rect.centerx, rect.top + self.images[0].get_height()//1.5]
            self.group.add(self.amo(self.images, pos,
                                    self.particle_group, [self.group]))
            return super().execute()
# -------------------------------------------------------------------


class Equipment:
    weaponIndex = 0

    def __init__(self, group, particle_group):
        self._weapon_equipment = []  # Weapons
        self._heal_equipment = []  # Heals
        self.isUltimateSelected = False
        self._group = group  # player`s shell group

        self._particle_group = particle_group
        self._weapon_equipment.append(
            FirstGun(self._group, self._particle_group))
        # self._weapon_equipment.append(
        #     DubleRedGun(self._group, self._particle_group))
        self._weapon_equipment.append(
            RocketLauncher(self._group, self._particle_group))
        self._weapon_equipment.append(
            BurnedLauncher(self._group, self._particle_group))
        self._ultimate = StrikeUltimate(
            self._group, self._particle_group)  # Ultimate

    def useUltimate(self, *args, **kwargs):
        self.isUltimateSelected = not self.isUltimateSelected
        self._ultimate.select(isUsed=self.isUltimateSelected)

    def changeWeapon(self, update=None, value=None):
        if not self.isUltimateSelected:
            if value:
                if 0 <= value-1 <= len(self._weapon_equipment)-1:
                    self.weaponIndex = value - 1
            elif update:
                if 0 <= update+self.weaponIndex <= len(self._weapon_equipment)-1:
                    self.weaponIndex += update
                elif update+self.weaponIndex < 0:
                    self.weaponIndex = len(self._weapon_equipment)-1
                elif update+self.weaponIndex > len(self._weapon_equipment)-1:
                    self.weaponIndex = 0

    def useWeapon(self, rect):
        if not self.isUltimateSelected:
            return self._weapon_equipment[self.weaponIndex].execute(rect)
        if self.isUltimateSelected:
            self._ultimate.execute()

    def useHeal(self):
        return

    def addWeapon(self, instance):
        self._weapon_equipment.append(instance)
        return self._weapon_equipment

    def addHeal(self, instance):
        self._heal_equipment.append(instance)
        return self._heal_equipment

    def setUltimate(self, instance):
        self._ultimate = instance
        return self._ultimate

    def countWeapons(self):
        return len(self._weapon_equipment)
