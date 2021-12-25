
from exception import NoneInitializeError
from animation import Animator
from player_equipment import Equipment
import pygame as pg
from pygame.sprite import Group, Sprite
from settings import IMAGES
from interface import HealthBar


class Player(Sprite):
    mediator = None
    animation = Animator
    equipment = Equipment  # heal, ultimate and weapon inventory*
    ability = None
    
    MAX_HP = 100
    HP = MAX_HP

    max_speed = 8.5
    xspeed = 0
    yspeed = 0
    accel = 0.4
    rect_color = (0, 255, 0)

    def __init__(self, display_size, mediator, shellGroup: Group, particle_group, *args, **kwargs):
        super().__init__()
        self.mediator = mediator
        self.health = HealthBar(
            [10, 10], self.MAX_HP, self.HP, [display_size[0]*0.45, display_size[1]*0.02], (228, 113, 116), background=(53, 64, 77), draw_text=True)
        self.animation = self.animation()
        self.equipment = self.equipment(shellGroup, particle_group)
        self.display_size = display_size

        self.images = {
            "default": [pg.image.load(
                IMAGES+'\player\space'+str(i)+'.png').convert_alpha() for i in range(1, 3)],
            "left": [pg.image.load(
                IMAGES+'\player\left'+str(i)+'.png').convert_alpha() for i in range(1, 3)],
            "right": [pg.image.load(
                IMAGES+'\player\\right'+str(i)+'.png').convert_alpha() for i in range(1, 3)]
        }
        self.acting_images = self.images['default']

        self.rect = self.acting_images[0].get_rect(
            center=self.spawn(display_size))
        self.rects = [
            pg.Rect(int(self.rect.left + self.rect.width/2.5), self.rect.top,
                    int(self.rect.width/5), int(self.rect.height*0.9)),
            pg.Rect(self.rect.left, int(self.rect.top +
                    self.rect.height/2.5), self.rect.width, self.rect.height/4)
        ]
        self.direction = pg.Vector2(0.0, 0.0)

    def spawn(self, dispaly_size):  # -> spawn pos
        return (dispaly_size[0] / 2, dispaly_size[1] / 2)

    def updatePosition(self, x_update=None, y_update=None):
        if not (x_update and y_update):

            if (self.rect.left + self.direction.x * self.xspeed > 0) and (self.rect.right + self.direction.x * self.xspeed < self.display_size[0]):
                self.rect.centerx += self.direction.x * self.xspeed
                for rect in self.rects:
                    rect.centerx += self.direction.x * self.xspeed

            if (self.rect.bottom + self.direction.y * self.yspeed < self.display_size[1] + 10) and (self.rect.top + self.direction.y * self.yspeed > 0):
                self.rect.centery += self.direction.y * self.yspeed
                for rect in self.rects:
                    rect.centery += self.direction.y * self.yspeed

        return self.rect

    def updateActingImage(self, threshold):
        if self.direction.x > threshold:
            self.acting_images = self.images['right']
        elif self.direction.x < -threshold:
            self.acting_images = self.images['left']
        else:
            self.acting_images = self.images['default']

        self.rect = self.acting_images[0].get_rect(center=self.rect.center)

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

    def update(self, *args, **kwargs):
        """Updating all player states"""
        self.updatePosition()
        self.updateActingImage(threshold=.35)
        self.animation.update(now=kwargs['now'], rate=80, frames_len=len(
            self.acting_images), repeat=True)

    def draw(self, dispaly):
        dispaly.blit(
            self.acting_images[self.animation.getIteration], self.rect)
        # for rect in self.rects:
        #     pg.draw.rect(dispaly, self.rect_color, rect, width=1)

        self.health.draw(dispaly, border_radius=self.rect.height//2, border_top_right_radius=self.rect.height//2)
        # self.health.draw(dispaly, border_bottom_right_radius=self.rect.height//2, border_top_right_radius=self.rect.height//2)

    def executeWeapon(self):
        return self.equipment.useWeapon(self.rect)

    def changeWeapon(self, value=None, update=None):
        return self.equipment.changeWeapon(value=value, update=update)

    def getHeal(self, object):  # -> new XP
        """Get size healing from object and use __heal method with healing parameters"""
        return self.__heal()

    def getRects(self):  # -> Rect
        return (self.rect, self.rects)

    def getHealth(self):
        return self.health.HP

    def damage(self, value):
        if self.HP - value > 0:
            self.HP -= value
        else:
            self.HP = 0
            
        self.health.updateHP(self.HP)

    def kill(self):
        return super().kill()
