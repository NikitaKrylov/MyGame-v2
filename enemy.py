from exception import NoneInitializeError
from animation import Animator, StaticMovement, CoordMovement, FunctionMovement
import pygame as pg
from pygame.sprite import Sprite, AbstractGroup
from settings import IMAGES
import random
import math
from interface import HealthBar


class AbstractEnemy(Sprite):  # Sprite Interface
    MAX_HP = 100
    HP = MAX_HP
    DAMAGE = 0
    animation = Animator
    ability = None

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(*groups)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center=pos)
        self.rects = [self.rect]
        self.animation = self.animation()
        self.direction = pg.Vector2(0.0, 0.0)

    def update(self, *args, **kwargs):
        self.updatePosition()

    def updatePosition(self, *args, **kwargs):
        pass

    def draw(self, display):
        display.blit(self.image, self.rect)
        # pg.draw.rect(display, (0, 255, 20), self.rect, width=3)

        # for rect in self.rects:
        #     pg.draw.rect(display, (0, 255, 0), rect, width=2)

    def getDamage(self):
        return self.DAMAGE

    def damage(self, amount):
        self.HP -= amount

        if self.HP <= 0:
            return self.kill()
        return self.HP

    def kill(self):
        return super().kill()


class Asteroid(AbstractEnemy):  # Sprite
    MAX_HP = 100
    HP = MAX_HP
    DAMAGE = 10

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.rot_speed = random.uniform(-1.0, 1.0)
        self.direction = pg.Vector2(0.0, 1.0)
        self.speed = self.generateSpeed()
        self.movement = StaticMovement(pg.Vector2(0, 1).rotate_rad(
            math.radians(random.randint(-35, 35))))
        self.rects = [self.image.get_rect(center=self.rect.center)]

    def generateSpeed(self):
        a = random.uniform(2, 7)
        if a > 6:
            a = random.uniform(5.5, 11)
        return a

    def updatePosition(self, *args, **kwargs):
        self.rect, _ = self.movement.update(
            self.rect,
            self.rects,
            speed=self.speed)

    def update(self, *args, **kwargs):
        self.rect, self.image, = self.animation.rotate(
            now=kwargs['now'],
            rot_speed=self.rot_speed,
            rect=self.rect,
            image=self.images[0],
            image_copy=self.image,
            cooldawn=15)

        self.updatePosition()
        self.rects[0].center = self.rect.center

        if kwargs.get('display_size'):
            if self.rect.top > kwargs['display_size'][1]:
                self.kill()
            elif self.rect.left > kwargs['display_size'][0]:
                self.kill()
            elif self.rect.right < 0:
                self.kill()

    def getDamage(self):
        self.kill()
        return super().getDamage()


class FirstFlightEnemy(AbstractEnemy):
    speed = 5
    MAX_HP = 250
    HP = MAX_HP
    DAMAGE = 15

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.movement = StaticMovement(pg.Vector2(1.0, 0.0))
        self.rects = [pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height*0.55),
                      pg.Rect(self.rect.x+self.rect.width/3, self.rect.y, self.rect.width//3, self.rect.height)]
        self.healthBar = HealthBar([self.rect.left, self.rect.top - self.rect.width*0.3],
                                   self.HP, self.MAX_HP, [self.rect.width, self.rect.height*0.11], (233, 22, 22))

    def update(self, *args, **kwargs):
        self.updatePosition()
        self.animation.update(
            now=kwargs['now'], rate=50, frames_len=len(self.images), repeat=True)
        self.image = self.images[self.animation.getIteration]

        if self.rect.left + self.direction.x * self.speed <= self.rect.width * -1.5:
            self.movement.changeDirection(mn_x=-1)

        if self.rect.right + self.direction.x * self.speed >= kwargs['display_size'][0] + self.rect.width*1.5:
            self.movement.changeDirection(mn_x=-1)

        self.healthBar.rect.x = self.rect.left
        self.healthBar.rect.y = self.rect.top - self.healthBar.rect.height * 1.5
        self.healthBar.HP = self.HP

    def updatePosition(self, *args, **kwargs):
        self.movement.update(
            self.rect,
            self.rects,
            speed=self.speed,
        )

    def draw(self, display):
        display.blit(self.image, self.rect)
        self.healthBar.draw(display)


class FirstFlightEnemy2(FirstFlightEnemy):
    speed = 1

    def __init__(self, images: list, pos: list, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        def func(x): return math.sin(x/50)*50 + 500
        self.movement = FunctionMovement(pg.Vector2(1.0, 0.0), func=func)

    def update(self, *args, **kwargs):
        self.updatePosition()
        self.animation.update(
            now=kwargs['now'], rate=50, frames_len=len(self.images), repeat=True)
        self.image = self.images[self.animation.getIteration]

        if self.rect.left + self.direction.x * self.speed <= self.rect.width * -1.5:
            self.movement.changeDirection(update_x=1)

        if self.rect.right + self.direction.x * self.speed >= kwargs['display_size'][0]+self.rect.width*1.5:
            self.movement.changeDirection(update_x=-1)

        self.healthBar.rect.x = self.rect.left
        self.healthBar.rect.y = self.rect.top - self.healthBar.rect.height * 1.5
        self.healthBar.HP = self.HP


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
    object = FirstFlightEnemy2

    def __init__(self, display_size, group=None, *args, **kwargs):
        super().__init__(display_size, group=group, *args, **kwargs)
        self.images = [pg.image.load(
            IMAGES+'\enemy\\firstFlight\\1Enemy'+str(i)+'.png').convert_alpha() for i in range(1, 3)]

    def createObject(self, *args, **kwargs):
        _obj = self.object(
            self.images, (-self.display_size[0]*0.1, self.display_size[1]//4), self.group)
        return super().createObject(*args, **kwargs)
