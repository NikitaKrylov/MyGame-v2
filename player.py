from typing import List, Tuple
from animation import Animator
from GameObjects.equipment import Equipment
import pygame as pg
from pygame.sprite import Group, Sprite
from changed_group import CustomGroup
from settings import IMAGES, PLAYER_HEALTHBAR_COLOR, PLAYER_HEALTHBAR_BACKGROUND_COLOR
from gui.interface import HealthBar
import logger
from GameObjects.prefabs import IEffect
from changed_group import Groups
from gui.interface import EquipmentDrawer

log = logger.get_logger(__name__)


# The player class is the main character of the game. It has abilities, weapons, and a set of
# animations
class Player(Sprite):

    MAX_HP = 100
    HP = MAX_HP

    max_speed = 7
    accel = 0.3
    isGodMod = False

    def __init__(self, display_size, shellGroup: Group, particle_group, *args, **kwargs):
        super().__init__()
        self.display_size = display_size
        self.HP = Player.MAX_HP
        self.health = HealthBar(
            [10, 10], self.HP, self.MAX_HP, [display_size[0]*0.35, display_size[1]*0.02], PLAYER_HEALTHBAR_COLOR, background=PLAYER_HEALTHBAR_BACKGROUND_COLOR, draw_text=True)
        self.shellGroup = shellGroup
        self.particle_group = particle_group

        self.equipment = Equipment(self.shellGroup, self.particle_group)
        EquipmentDrawer(self.equipment).add(Groups.Interface)
        self.movement = MovementLogic(display_size, self.max_speed, self.accel)
        self.animation = Animator()
        self.effectsGroup = EffectsGroup()
        self.spaceship = DefaultSpaceShip()
        self.spaceship.CreateRects(self.spawn(self.display_size))

# ------------------------------MOVEMENT AND DRAWING--------------------------------------

    def spawn(self, dispaly_size):
        return (dispaly_size[0] / 2, dispaly_size[1] / 2)

    def increaseAccel(self, axis):
        self.movement.increaseAccel(axis)

    def decreaseAccel(self, axis):
        self.movement.decreaseAccel(axis)

    def update(self, *args, **kwargs):
        """Updating all player states"""
        self.effectsGroup.update()
        self.rect, self.rects = self.movement.UpdatePosition(
            self.rect, self.rects)
        self.spaceship.UpdateActingImage(self.movement.direction, 0.35)
        self.animation.update(rate=80, frames_len=len(
            self.spaceship.acting_images), repeat=True)

    def draw(self, display):
        display.blit(
            self.spaceship.acting_images[self.animation.getIteration], self.spaceship.GetRect())
        self.health.draw(display, border_radius=self.rect.height //
                         2, border_top_right_radius=self.rect.height//2)
        self.effectsGroup.draw(display)

# ------------------------------WEAPONS--------------------------------------

    def executeWeapon(self):
        if self.equipment.isUltimateSelected:
            return self.equipment.UseUltimate(self)
        return self.equipment.UseWeapon(self.rect)

    def changeWeapon(self, value=None, update=None):
        return self.equipment.SelectObject(value=value, update=update)

    def changeUltimate(self):
        print("change")

    def selectUltimate(self):
        self.equipment.SelectUltimate(self)

    def damage(self, value):
        if not self.isGodMod:
            if self.HP - value > 0:
                self.HP -= value
            else:
                self.HP = 0

            self.health.updateHP(self.HP)

    def AddForce(self, direction: pg.Vector2, force=None, *args, **kwargs):

        self.rect, self.rects = self.movement.AddForce(
            self.rect, force, *args, **kwargs)

    def ReactToDamage(self, *args, **kwargs):
        if not self.isGodMod:

            if kwargs.get('enemy_rect') and kwargs.get('direction'):
                if self.rect.centery > kwargs['enemy_rect'].centery:
                    kwargs['direction'].y = 1
                elif self.rect.centery < kwargs['enemy_rect'].centery:
                    kwargs['direction'].y = -1

            self.AddForce(*args, **kwargs)

    def AddEffect(self, effect):
        self.effectsGroup.add(effect)


# ------------------------------OTHER--------------------------------------

    @property
    def rect(self):
        return self.spaceship.GetRect()

    @rect.setter
    def rect(self, value: pg.Rect):
        self.spaceship.rect = value

    @property
    def rects(self):
        return self.spaceship.GetRects()

    @rects.setter
    def rects(self, value: List[pg.Rect]):
        self.spaceship.rects = value

    def SetGodMode(self, value: bool = None):
        self.isGodMod = value if value is not None else not self.isGodMod

    def restart(self):
        self.__init__(self.display_size, self.shellGroup, self.particle_group)

# -------------------------------------------------------


class EffectsGroup(CustomGroup):
    def __init__(self, *sprites: Tuple[IEffect]):
        super().__init__(*sprites)

    def empty(self):
        for ef in self.sprites():
            pass
        return super().empty()
# -------------------------------------------------------


class MovementLogic:
    def __init__(self, display_size, max_speed,  acceleration: float = 1):
        self.direction = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(0, 0)
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.display_size = display_size

    def UpdatePosition(self, rect, rects, x_update=None, y_update=None):
        if not (x_update and y_update):
            if (rect.left + self.direction.x * self.velocity.x > 0) and (rect.right + self.direction.x * self.velocity.x < self.display_size[0]):
                rect.centerx += self.direction.x * self.velocity.x

            if (rect.bottom + self.direction.y * self.velocity.y < self.display_size[1] + 10) and (rect.top + self.direction.y * self.velocity.y > 0):
                rect.centery += self.direction.y * self.velocity.y

        rects = [
            pg.Rect(int(rect.left + rect.width/2.5), rect.top,
                    int(rect.width/5), int(rect.height*0.9)),
            pg.Rect(rect.left, int(rect.top +
                    rect.height/2.5), rect.width, rect.height/4)
        ]

        return (rect, rects)

    def increaseAccel(self, axis):
        if axis == 0:
            _direction = self.direction.x
            _speed = self.velocity.x
        elif axis == 1:
            _direction = self.direction.y
            _speed = self.velocity.y

        if _speed + self.acceleration < self.max_speed:
            _speed += self.acceleration

        if axis == 0:
            self.direction.x = _direction
            self.velocity.x = _speed
        elif axis == 1:
            self.direction.y = _direction
            self.velocity.y = _speed

    def decreaseAccel(self, axis):
        if axis == 0:
            _direction = self.direction.x
            _speed = self.velocity.x
        elif axis == 1:
            _direction = self.direction.y
            _speed = self.velocity.y

        if _speed - self.acceleration > 0:
            _speed -= self.acceleration
        else:
            _speed = 0
            _direction = 0

        if axis == 0:
            self.direction.x = _direction
            self.velocity.x = _speed
        elif axis == 1:
            self.direction.y = _direction
            self.velocity.y = _speed

    def AddForce(self, rect: pg.Rect, force=None, *args, **kwargs):
        _force = force if force is not None else rect.height * 2

        if rect.bottom + _force < self.display_size[1]:
            rect.centery += _force
        else:
            rect.centery -= _force

        rects = [
            pg.Rect(int(rect.left + rect.width/2.5), rect.top,
                    int(rect.width/5), int(rect.height*0.9)),
            pg.Rect(rect.left, int(rect.top +
                                   rect.height/2.5), rect.width, rect.height/4)
        ]

        return rect, rects

# -------------------------------------------------------


class ISpaceShip:
    rect: pg.Rect = None
    rects: List[pg.Rect] = []
    acting_images = None

    def __init__(self):
        pass

    def CreateRects(self):
        pass

    def UpdateRects(self):
        pass

    def GetRect(self):
        return self.rect

    def GetRects(self):
        return self.rects

    def UpdateActingImage(self, direction, threshold):
        self.rect = self.acting_images[0].get_rect(center=self.rect.center)
        self.UpdateRects()


class DefaultSpaceShip(ISpaceShip):
    def __init__(self):
        super().__init__()
        self.images = {
            "default": [pg.image.load(
                IMAGES+'\player\space'+str(i)+'.png').convert_alpha() for i in range(1, 3)],
            "left": [pg.image.load(
                IMAGES+'\player\left'+str(i)+'.png').convert_alpha() for i in range(1, 3)],
            "right": [pg.image.load(
                IMAGES+'\player\\right'+str(i)+'.png').convert_alpha() for i in range(1, 3)]
        }
        self.acting_images = self.images.get("default")

    def CreateRects(self, center):
        self.rect = self.acting_images[0].get_rect(center=center)

        self.rects = [
            pg.Rect(int(self.rect.left + self.rect.width/2.5), self.rect.top,
                    int(self.rect.width/5), int(self.rect.height*0.9)),
            pg.Rect(self.rect.left, int(self.rect.top +
                    self.rect.height/2.5), self.rect.width, self.rect.height/4)
        ]
        return super().CreateRects()

    def UpdateRects(self):
        self.rects = [
            pg.Rect(int(self.rect.left + self.rect.width/2.5), self.rect.top,
                    int(self.rect.width/5), int(self.rect.height*0.9)),
            pg.Rect(self.rect.left, int(self.rect.top +
                    self.rect.height/2.5), self.rect.width, self.rect.height/4)
        ]
        return self.rects

    def UpdateActingImage(self, direction, threshold):
        if direction.x > threshold:
            self.acting_images = self.images['right']
        elif direction.x < -threshold:
            self.acting_images = self.images['left']
        else:
            self.acting_images = self.images['default']

        return super().UpdateActingImage(direction, threshold)
