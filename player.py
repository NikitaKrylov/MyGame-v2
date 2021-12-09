
from exception import NoneInitializeError
from animation import Animator
from player_equipment import Equipment
import pygame as pg
from pygame.sprite import Group, Sprite


class Player(Sprite):
    mediator = None
    MAX_XP = None
    XP = MAX_XP
    __animation = Animator
    equipment = Equipment  # heal, ultimate and weapon inventory*
    ability = None

    max_speed = 9.0
    xspeed = 0
    yspeed = 0
    accel = 0.45

    def __init__(self, display_size, mediator, *args, **kwargs):
        super().__init__()
        self.mediator = mediator
        self.width, self.height = 80, 150
        self.surface = pg.Surface((self.width, self.height))
        self.surface.fill('red')

        self.rect = self.surface.get_rect(center=self.spawn(display_size))
        # self.rect = pg.Rect(self.spawn(display_size),
        #                     (self.width, self.height))
        self.rects = []
        self.direction = pg.Vector2(0.0, 0.0)

    def spawn(self, dispaly_size):  # -> spawn pos
        return (dispaly_size[0] / 2, dispaly_size[1] / 2)

    def updatePosition(self, x_update=None, y_update=None):
        if not (x_update and y_update):
            self.rect.centerx += self.direction.x * self.xspeed
            self.rect.centery += self.direction.y * self.yspeed

        return self.rect

    def increaseAccel(self, axis):
        if axis == 0:
            _direction = self.direction.x
            _speed = self.xspeed
        elif axis == 1:
            _direction = self.direction.y
            _speed = self.yspeed

        if _speed + self.accel < self.max_speed:
            _speed += self.accel

        if axis == 0:
            self.direction.x = _direction
            self.xspeed = _speed
        elif axis == 1:
            self.direction.y = _direction
            self.yspeed = _speed

    def decreaseAccel(self, axis):
        if axis == 0:
            _direction = self.direction.x
            _speed = self.xspeed
        elif axis == 1:
            _direction = self.direction.y
            _speed = self.yspeed

        if _speed - self.accel > 0:
            _speed -= self.accel
        else:
            _speed = 0
            _direction = 0

        if axis == 0:
            self.direction.x = _direction
            self.xspeed = _speed
        elif axis == 1:
            self.direction.y = _direction
            self.yspeed = _speed

    def updateAccel(self, axis):
        pass

    def updateAnimation(self):
        pass

    def update(self, *args, **kwargs):
        self.updatePosition()

    def draw(self, dispaly):
        dispaly.blit(self.surface, self.rect)

    def getDamage(self):  # функция наносит урон игроку -> damage received, remaining HP
        pass

    def toDamage(self):
        pass
    
    def executeWeapon(self):
        return print('Я сделал выстрел!')

    def useUltimate(self):
        pass

    def changeUltimate(self):
        pass

    def changeAmo(self):
        pass

    def changeWeapon(self):
        pass

    def getHeal(self, object):  # -> new XP
        """Get size healing from object and use __heal method with healing parameters"""
        return self.__heal()

    def getRects(self):  # -> Rect
        pass

    def __heal(self, sizeH):  # -> new XP
        self.XP += sizeH
        pass

    def kill(self):
        pass
