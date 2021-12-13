from exception import NoneInitializeError
from animation import Animator
import pygame as pg
from pygame.sprite import Sprite, AbstractGroup
from settings import IMAGES
import random
import math



class AbstractEnemy(Sprite):  # Sprite Interface
    XP = 1000
    animation = Animator
    ability = None

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(*groups)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center=pos)
        self.animation = self.animation()
        self.burstAnimation = self.animation()
        self.direction = pg.Vector2(0.0, 0.0)

    def updatePosition(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        return self.rect

    def update(self, *args, **kwargs):
        self.updatePosition()

    def kill(self):
        return super().kill()

    def __str__(self):
        return self.__class__.__name__


class Asteroid(AbstractEnemy):  # Sprite
    speed = 4

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.rot_speed = random.uniform(-1.0, 1.0)
        self.direction = pg.Vector2(0.0, 1.0)
        self.direction = self.direction.rotate_rad(
            math.radians(random.randint(-35, 35)))
        self.speed = self.generateSpeed()

    def generateSpeed(self):
        a = random.uniform(2, 7)
        if a > 6:
            a = random.uniform(5.5, 11)
        return a

    def update(self, *args, **kwargs):
        self.rect, self.image, = self.animation.rotate(
            now=kwargs['now'],
            rot_speed=self.rot_speed,
            rect=self.rect,
            image=self.images[0],
            image_copy=self.image,
            cooldawn=15)

        self.updatePosition()

        if kwargs.get('display_size'):
            if self.rect.top > kwargs['display_size'][1]:
                self.kill()
            elif self.rect.left > kwargs['display_size'][0]:
                self.kill()
            elif self.rect.right < 0:
                self.kill()


class FirstFlightEnemy(AbstractEnemy):
    speed = 5

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.direction = pg.Vector2(1.0, 0.0)

    def update(self, *args, **kwargs):
        self.animation.update(
            now=kwargs['now'], rate=50, frames_len=len(self.images), repeat=True)
        self.image = self.images[self.animation.getIteration]

        if self.rect.left + self.direction.x * self.speed <= 0:
            self.direction.x *= -1

        if self.rect.right + self.direction.x * self.speed >= kwargs['display_size'][0]:
            self.direction.x *= -1

        return super().update(*args, **kwargs)


# -----------------------------------------------------------------

class AbstarctFactory:
    object = None

    def __init__(self, display_size, group=None, *args, **kwargs):
        self.display_size = display_size
        self.group = group

    def createObject(self, *args, **kwargs):
        """create and add object to group"""
        pass

    def count(self):  # -> int
        counter = 0
        for sprite in self.group.sprites():
            if isinstance(sprite, self.object):
                counter += 1

        return counter

    def updateAllObjectCondition(self, func):
        """apply fuction to all gropu object 
        for example, change damage
        """
        pass

    def __destroyAllObject(self):
        pass


# ------------------------------------------------------------------


class AsteroidFactory(AbstarctFactory):
    object = Asteroid

    def __init__(self, display_size, group=None,  *args, **kwargs):
        super().__init__(display_size, group=group, *args, **kwargs)
        self.all_images = [pg.image.load(
            IMAGES+'\enemy\\asteroid\\asteroid'+str(i)+'.png').convert_alpha() for i in range(1, 7)]

    def createObject(self, *args, **kwargs):
        random_image = random.choice(self.all_images)
        spawn_pos = (random.randint(
            10, self.display_size[0]), -random_image.get_rect().height)
        _obj = self.object([random_image], spawn_pos, self.group)
        return super().createObject(*args, **kwargs)


class FirstFlightEnemyFactory(AbstarctFactory):
    object = FirstFlightEnemy

    def __init__(self, display_size, group=None, *args, **kwargs):
        super().__init__(display_size, group=group, *args, **kwargs)
        self.images = [pg.image.load(
            IMAGES+'\enemy\\firstFlight\\1Enemy'+str(i)+'.png').convert_alpha() for i in range(1, 3)]

    def createObject(self, *args, **kwargs):
        _obj = self.object(
            self.images, (self.display_size[0]//6, self.display_size[1]//4), self.group)
        return super().createObject(*args, **kwargs)
