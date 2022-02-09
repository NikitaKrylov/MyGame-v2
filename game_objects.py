
import pygame as pg
from typing import Union, Tuple, List, Sequence
from pygame.sprite import Sprite, AbstractGroup
from sprites.shell import BaseShell, BurnedShell, FirstShell, RedEnemyShell, Rocket, RedShell, StarEnemyShell, Strike
from settings import IMAGES
from timer import Timer
from GameObjects.weapons import RocketLauncher, LiteGun, BurnedLauncher, IWeapon
from GameObjects.ultimates import IUltimate, Striker


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
        self.label_image = None
        self.__isExecute = True
        self.updatingTime = {
            'last': 0,
            'cooldawn': 0
        }

    def GetCooldawnDelta(self):
        return None

    def execute(self, *args, **kwargs):
        pass

    @property
    def isExecute(self):
        now = Timer.get_ticks()
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

    def execute(self, player=None, *args, **kwargs):
        return super().execute(*args, **kwargs)


class EffectUltimate(AbstractUltimate):
    duration = None
    instance = None

    def __init__(self, group, particle_group):
        super().__init__(group, particle_group)

# -----------------------------------


class AimingPoint(Sprite):
    """Hover point class used with some ultimates"""

    def __init__(self, image, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(center=pg.mouse.get_pos())
        # self.movement = StaticMovement(pg.Vector2(0, 0))

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


# -----------------------------


class StrikeUltimate(AbstractUltimate):

    instance = None
    amo = Strike

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

    def select(self, isUsed, *args, **kwargs):
        if not isUsed and self.instance != None:
            self.instance.kill()
            self.instance = None

        if isUsed and self.instance == None:
            self.instance = AimingPoint(self.image)
            self.particle_group.add(self.instance)

        return super().select(isUsed, *args, **kwargs)

    def execute(self, player=None, *args, **kwargs):
        if self.isExecute:
            image = pg.Surface((100, 100))
            image.fill((255, 90, 20))
            obj = self.amo([image], self.instance.rect.center,
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


# class FirstGun(AbstractGun):
#     amo = FirstShell

#     def __init__(self, group, particle_group):
#         super().__init__(group, particle_group)
#         self.images = [pg.image.load(
#             IMAGES+'\shell\lite\shell'+str(i)+'.png').convert_alpha() for i in range(1, 6)]
#         self.label_image = pg.image.load(
#             IMAGES+'\\menu\\labels\\lite.png').convert_alpha()

#     def execute(self, rect, *args, **kwargs):
#         pos = [rect.centerx, int(rect.top+self.images[0].get_rect().height//2)]
#         self.group.add(self.amo(self.images, pos,
#                        self.particle_group, [self.group]))
#         return super().execute()


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
            'cooldawn': 1000
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


# class RocketLauncher(AbstractGun):
#     amo = Rocket

#     def __init__(self, group, particle_group):
#         super().__init__(group, particle_group)
#         # self.images = [pg.image.load(
#         # IMAGES+'\shell\\racket\\racket'+str(i)+'.png').convert_alpha() for i in range(1, 7)]
#         self.images = [pg.image.load(
#             IMAGES+'\shell\\racket\\racket.png').convert_alpha()]
#         self.updatingTime = {
#             'last': 0,
#             'cooldawn': 1000
#         }

#     def execute(self, rect, *args, **kwargs):
#         if self.isExecute:
#             self.group.add(self.amo(self.images, rect.center,
#                                     self.particle_group, [self.group]))
#             return super().execute()


# class BurnedLauncher(AbstractGun):
#     amo = BurnedShell

#     def __init__(self, group, particle_group):
#         super().__init__(group, particle_group)
#         self.updatingTime = {
#             'last': 0,
#             'cooldawn': 100
#         }
#         self.images = [pg.image.load(
#             IMAGES+'\shell\\orange\\orange.png').convert_alpha()]

#     def execute(self, rect, *args, **kwargs):
#         if self.isExecute:
#             pos = [rect.centerx, rect.top + self.images[0].get_height()//1.5]
#             self.group.add(self.amo(self.images, pos,
#                                     self.particle_group, [self.group]))
#             return super().execute()
# # -------------------------------------------------------------------


# class Equipment:
#     weaponIndex = 0

#     def __init__(self, group, particle_group):
#         self._weapon_equipment = []  # Weapons
#         self._heal_equipment = []  # Heals
#         self.isUltimateSelected = False
#         self._group = group  # player`s shell group

#         self._particle_group = particle_group
#         self._weapon_equipment.append(
#             LiteGun(self._group, self._particle_group))
#         # self._weapon_equipment.append(
#         #     DubleRedGun(self._group, self._particle_group))
#         self._weapon_equipment.append(
#             RocketLauncher(self._group, self._particle_group))
#         self._weapon_equipment.append(
#             BurnedLauncher(self._group, self._particle_group))
#         self._ultimate = StrikeUltimate(
#             self._group, self._particle_group)  # Ultimate

#     def selectUltimate(self, *args, **kwargs):
#         self.isUltimateSelected = not self.isUltimateSelected
#         self._ultimate.select(isUsed=self.isUltimateSelected)

#     def changeWeapon(self, update=None, value=None):
#         if self.isUltimateSelected:
#             self.isUltimateSelected = False
#             self._ultimate.select(isUsed=self.isUltimateSelected)

#         if value:
#             if 0 <= value-1 <= len(self._weapon_equipment)-1:
#                 self.weaponIndex = value - 1
#         elif update:
#             if 0 <= update+self.weaponIndex <= len(self._weapon_equipment)-1:
#                 self.weaponIndex += update
#             elif update+self.weaponIndex < 0:
#                 self.weaponIndex = len(self._weapon_equipment)-1
#             elif update+self.weaponIndex > len(self._weapon_equipment)-1:
#                 self.weaponIndex = 0

#     def useWeapon(self, rect):
#         if not self.isUltimateSelected:
#             return self._weapon_equipment[self.weaponIndex].execute(rect)

#     def useUltimate(self, player, *args, **kwargs):
#         if self.isUltimateSelected:
#             self._ultimate.execute(player, *args, **kwargs)

#     def useHeal(self):
#         return

#     def addWeapon(self, instance):
#         self._weapon_equipment.append(instance)
#         return self._weapon_equipment

#     def addHeal(self, instance):
#         self._heal_equipment.append(instance)
#         return self._heal_equipment

#     def setUltimate(self, instance):
#         self._ultimate = instance
#         return self._ultimate

#     def countWeapons(self):
#         return len(self._weapon_equipment)


class Equipment:
    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        self._group = group
        self._particle_group = particle_group
        
        self.weaponIndex = 0
        self._weapon_equipment: List[IWeapon] = []
        self._heal_equipment = []
        self._ultimate: IUltimate = None
        self.isUltimateSelected = False

        self.AddWeapon(LiteGun, RocketLauncher, BurnedLauncher)
        self.AddUltimate(Striker)

    def SelectUltimate(self):
        pass

    def SelectWeapon(self):
        pass

    def SelectObject(self, update=None, value=None):
        if self.isUltimateSelected:
            self.isUltimateSelected = False
            self._ultimate.Select(isUsed=self.isUltimateSelected)

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

    def UseWeapon(self, rect, *args, **kwargs):
        self._weapon_equipment[self.weaponIndex].Use(rect)

    def UseUltimate(self):
        pass

    def UseObject(self, rect, *args, **kwargs):
        if self.isUltimateSelected:
            return self.UseUltimate()

        return self.UseWeapon(rect, *args, **kwargs)

    def AddWeapon(self, *prefabs:Tuple[IWeapon]):
        for prefab in prefabs:
            self._weapon_equipment.append(
                prefab(group=self._group, particle_group=self._particle_group))
    def AddUltimate(self, prefabs:IUltimate):
        self._ultimate = prefabs(group=self._group, particle_group=self._particle_group)

    def countWeapons(self):
        return len(self._weapon_equipment)
