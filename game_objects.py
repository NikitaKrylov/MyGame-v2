import pygame as pg
from animation import Animator
from sprites.shell import *
from pygame.sprite import Sprite, AbstractGroup
from sprites.shell import BaseShell
from pygame.sprite import Group
from settings import IMAGES


class ObjectInterface(Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)

    def execute(self):
        pass

    def draw(self, display, *args, **kwargs):
        pass

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

    def execute(self):
        return

    @property
    def isExecute(self):
        now = pg.time.get_ticks()
        if now - self.updatingTime['last'] > self.updatingTime['cooldawn']:
            self.updatingTime['last'] = now
            return True
        return False


class AbstractUltimate:
    def __init__(self):
        pass

    def execute(self):
        return


class AbstractGun(AbstaructWeapon):
    amo = BaseShell

    def __init__(self, group, particle_group):
        super().__init__()
        self.particle_group = particle_group
        self.group = group

    def execute(self):
        return super().execute()


class FirstGun(AbstractGun):
    amo = FirstShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.images = [pg.image.load(
            IMAGES+'\shell\lite\shell'+str(i)+'.png').convert_alpha() for i in range(1, 6)]

    def execute(self, rect):
        pos = [rect.centerx, int(rect.top+self.images[0].get_rect().height//2)]
        self.group.add(self.amo(self.images, pos,
                       self.particle_group, [self.group]))
        return super().execute()


class DubleGun(AbstractGun):
    amo = SecondShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.images = [pg.image.load(
            IMAGES+'\shell\\red\\redshell'+str(i)+'.png').convert_alpha() for i in range(1, 6)]

    def execute(self, rect):
        pos1 = [rect.left, rect.top+rect.height//2]
        pos2 = [rect.right, pos1[1]]
        self.group.add(self.amo(self.images, pos1,
                       self.particle_group, [self.group]))
        self.group.add(self.amo(self.images, pos2,
                       self.particle_group, [self.group]))
        return super().execute()


class DubleGunEnemy(DubleGun):
    amo = SecondShellEnemy

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.updatingTime = {
            'last': 0,
            'cooldawn': 1700
        }

    def execute(self, rect):
        if self.isExecute:
            pos1 = [rect.left, rect.top+rect.height//2]
            pos2 = [rect.right, pos1[1]]
            self.group.add(self.amo(self.images, pos1,
                                    self.particle_group, [self.group]))
            self.group.add(self.amo(self.images, pos2,
                                    self.particle_group, [self.group]))
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

    def execute(self, rect):
        if self.isExecute:
            self.group.add(self.amo(self.images, rect.center,
                                    self.particle_group, [self.group]))
            return super().execute()


class BurnedLauncher(AbstractGun):
    amo = BurnedShell

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)
        self.images = [pg.image.load(
            IMAGES+'\shell\\orange\\orange.png').convert_alpha()]

    def execute(self, rect):
        pos = [rect.centerx, rect.top + self.images[0].get_height()//1.5]
        self.group.add(self.amo(self.images, pos,
                       self.particle_group, [self.group]))
        return super().execute()
# -------------------------------------------------------------------


class Equipment:
    _weapon_equipment = []  # Weapons
    weaponIndex = 0
    _heal_equipment = []  # Heals
    _ultimate = None  # Ultimates
    _group = None  # player`s shell group

    def __init__(self, group, particle_group):
        self._group = group
        self._particle_group = particle_group
        self._weapon_equipment.append(
            FirstGun(self._group, self._particle_group))
        self._weapon_equipment.append(
            DubleGun(self._group, self._particle_group))
        self._weapon_equipment.append(
            RocketLauncher(self._group, self._particle_group))
        self._weapon_equipment.append(
            BurnedLauncher(self._group, self._particle_group))

    def useUltimate(self):
        self._ultimate.use()

    def changeWeapon(self, update=None, value=None):
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
        return self._weapon_equipment[self.weaponIndex].execute(rect)

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
