from animation import Animator, StaticMovement, FunctionMovement, PointerMovement
import pygame as pg
from pygame.sprite import Sprite, AbstractGroup
from settings import IMAGES, ENEMY_HEALTHBAR_COLOR
import random
import math
from gui.interface import HealthBar
from GameObjects.weapons import SingleRedGunEnemy, StarGun
from AI import WanderingAI


def sign(value):
    return 1 if value > 0 else -1


# The IEnemy class is an interface for all enemies in the game.
# It defines the basic attributes and methods that all enemies must have.
class IEnemy(Sprite):
    MAX_HP = 100
    HP = MAX_HP
    DAMAGE = 0
    animation = Animator
    ability = None
    isDamage = True
    isBurst = False

    def __init__(self, images: list, pos: list, factory, *groups: AbstractGroup, **kwargs):
        super().__init__(*groups)
        self.factory = factory
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center=pos)
        self.rects = [self.rect]
        self.animation = self.animation()
        self.movement = None

        if kwargs.get('burst_images'):
            self.burst_images = kwargs.get('burst_images')
        if kwargs.get('particle_group'):
            self.particle_group = kwargs.get('particle_group')

    def update(self, *args, **kwargs):
        self.updatePosition(*args, **kwargs)

    def updatePosition(self, *args, **kwargs):
        pass

    def draw(self, display):
        display.blit(self.image, self.rect)
        # pg.draw.rect(display, (0, 255, 20), self.rect, width=3)

        # for rect in self.rects:
        #     pg.draw.rect(display, (255, 0, 0), rect, width=2)

    def getDamage(self):
        if self.isDamage:
            return self.DAMAGE
        return 0

    def damage(self, amount):
        self.HP -= amount

        if self.HP <= 0:
            self.factory.spriteWasKilled(self)
            super().kill()
            return False
        return self.HP


class Asteroid(IEnemy):
    MAX_HP = 70
    HP = MAX_HP
    DAMAGE = 10

    def __init__(self, images: list, pos: list, factory, *groups: AbstractGroup, **kwargs):
        scale_index = random.uniform(0.7, 1.7)
        images = [pg.transform.scale(image, (int(image.get_width(
        )*scale_index), int(image.get_height() * scale_index))) for image in images]
        self.DAMAGE = int(self.DAMAGE * scale_index)
        self.HP = int(self.HP * scale_index)
        super().__init__(images, pos, factory, *groups, **kwargs)
        self.rot_speed = random.uniform(-1.0, 1.0)
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
            rot_speed=self.rot_speed,
            rect=self.rect,
            image=self.images[0],
            image_copy=self.image,
            cooldawn=15)

        if self.isBurst:
            self.animation.update(rate=100, frames_len=len(
                self.burst_images), repeat=False, finiteFunction=self.kill)
            self.image = self.burst_images[self.animation.getIteration]
            return

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
        self.isBurst = True
        _damage = super().getDamage()
        self.isDamage = False

        return _damage

    def damage(self, amount):
        self.HP -= amount

        if self.HP <= 0:
            self.factory.spriteWasKilled(self)
            self.isBurst = True

    def kill(self):
        self.factory.spriteWasDestroy(self)
        return super().kill()


class IInertial:
    pass



class AbstaractFlightEnemy(IEnemy, IInertial):
    speed = 5
    MAX_HP = 250
    HP = MAX_HP
    DAMAGE = 5

    def __init__(self, images: list, pos: list, factory, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, factory, *groups, **kwargs)
        self.rects = [pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height*0.55),
                      pg.Rect(self.rect.x+self.rect.width/3, self.rect.y, self.rect.width//3, self.rect.height)]
        self.healthBar = HealthBar([self.rect.left, self.rect.top - self.rect.width*0.3],
                                   self.HP, self.MAX_HP, [self.rect.width, self.rect.height*0.09], ENEMY_HEALTHBAR_COLOR)
        self.movement = None
        self.weapon = SingleRedGunEnemy(
            self.groups()[0], kwargs.get('particle_group'))
        self.burstAnimation = Animator()

    def damage(self, amount):
        self.HP -= amount
        self.healthBar.updateHP(self.HP)

        if self.HP <= 0 and not self.isBurst:
            self.factory.spriteWasKilled(self)
            self.isDamage = False
            self.isBurst = True
            return False
        else:
            return self.HP

    def updatePosition(self, *args, **kwargs):
        self.movement.update(
            self.rect,
            self.rects,
            speed=self.speed,
        )

    def update(self, *args, **kwargs):

        self.animation.update(
            rate=50, frames_len=len(self.images), repeat=True)

        if self.isBurst:
            self.burstAnimation.update(rate=80, frames_len=len(
                self.burst_images), repeat=False, finiteFunction=self.kill)
            self.image = self.burst_images[self.burstAnimation.getIteration]
            return

        self.image = self.images[self.animation.getIteration]
        self.healthBar.update(self.rect.left, self.rect.top -
                              self.healthBar.rect.height * 1.5)

        self.weapon.Use(self.rect)

        return super().update(*args, **kwargs)  # updatePosition()

    def draw(self, display):
        self.healthBar.draw(display)
        return super().draw(display)


class FirstFlightEnemy2(AbstaractFlightEnemy):
    speed = 1  # dont float!

    def __init__(self, images: list, pos: list, factory, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, factory, *groups, **kwargs)
        self._a, self._b = random.randint(60, 120), random.randint(30, 90)
        self.bias = pos[1]
        def func(x): return math.sin(x/self._a)*self._b + self.bias
        self.speed = random.randint(1, 2)
        self.movement = FunctionMovement(pg.Vector2(1.0, 1.0), func=func)

    def update(self, *args, **kwargs):
        if self.rect.left + self.movement.direction.x * self.speed <= self.rect.width * -1.5:
            self.movement.changeDirection(update_x=1)
            self.bias += self.rect.height * self.movement.direction.y

        if self.rect.right + self.movement.direction.x * self.speed >= kwargs['display_size'][0]+self.rect.width*1.5:
            self.movement.changeDirection(update_x=-1)
            self.bias += self.rect.height * self.movement.direction.y

        if self.rect.centery > kwargs['display_size'][1] - self.rect.width * 4 and self.movement.direction.y > 0:
            self.movement.changeDirection(update_y=-1)
            self.movement.func = lambda x: math.sin(
                x/self._a)*self._b + self.bias

        if self.rect.centery < self.rect.width * 1.5 and self.movement.direction.y < 0:
            self.movement.changeDirection(update_y=1)
            self.movement.func = lambda x: math.sin(
                x/self._a)*self._b + self.bias

        return super().update(*args, **kwargs)


class StarEnemy(IEnemy, IInertial):
    speed = 1.5
    MAX_HP = 300
    HP = MAX_HP
    DAMAGE = 5

    def __init__(self, images: list, pos: list, factory, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, factory, *groups, **kwargs)
        self.rects = [images[0].get_rect(center=pos)]
        self.rot_speed = .8
        self.healthBar = HealthBar([self.rect.left, self.rect.top - self.rect.width*0.3],
                                   self.HP, self.MAX_HP, [self.rect.width, self.rect.height*0.11], ENEMY_HEALTHBAR_COLOR)
        self.movement = PointerMovement(pg.Vector2(1, 0))
        self.weapon = StarGun(self.groups()[0], kwargs.get('particle_group'))
        self.brain = WanderingAI(self.updateState1)

    def update(self, *args, **kwargs):
        self.brain.Update(*args, **kwargs)
        return super().update(*args, **kwargs)

    def defaultUpdate(self, *args, **kwargs):
        if self.isBurst:
            self.kill()
            return

        self.rect, self.image, = self.animation.rotate(
            rot_speed=self.rot_speed,
            rect=self.rect,
            image=self.images[0],
            image_copy=self.image,
            cooldawn=15)

        self.updatePoints(kwargs['display_size'])

        self.healthBar.update(self.rects[0].left, self.rects[0].top -
                              self.healthBar.rect.height)

        self.movement.update(self.rect, self.rects, speed=self.speed)

    def updateState1(self, *args, **kwargs):
        if self.weapon.isExecute:
            for i in range(0, 361, 90):
                v = self.animation.rotVector.rotate_rad(math.radians(i))
                v.scale_to_length(self.rect.width//2.5)
                point_pos = (self.rect.centerx + v.x, self.rect.centery + v.y)
                v.scale_to_length(1)
                self.weapon.Use(self.rect, pos=point_pos, vector=v)

        if self.HP < self.MAX_HP/3:
            self.brain.Push(self.updateState2)

        self.defaultUpdate(*args, **kwargs)

    def updateState2(self, *args, **kwargs):
        if self.weapon.isExecute:
            for i in range(0, 361, 40):
                v = self.animation.rotVector.rotate_rad(math.radians(i))
                v.scale_to_length(self.rect.width//2.5)
                point_pos = (self.rect.centerx + v.x, self.rect.centery + v.y)
                v.scale_to_length(1)
                self.weapon.Use(self.rect, pos=point_pos, vector=v)

        if self.HP > self.MAX_HP/3:
            self.brain.Pop()

        self.defaultUpdate(*args, **kwargs)

    def updatePoints(self, display_size, *args, **kwargs):
        if not self.movement.next_point:
            point = self.createPoints(display_size)
            self.movement.next_point = point

        if not self.movement.point:
            point = self.createPoints(display_size)
            self.movement.point = point
        return

    def createPoints(self, display_size, *args, **kwargs):
        return [random.randint(0, display_size[0]),
                random.randint(0, display_size[1])]

    def damage(self, amount):
        self.HP -= amount
        self.healthBar.updateHP(self.HP)

        if self.HP <= 0 and not self.isBurst:
            self.factory.spriteWasKilled(self)
            self.isDamage = False
            self.isBurst = True

            super().kill()
            return
        else:
            return self.HP

    def draw(self, display):
        self.healthBar.draw(display)
        return super().draw(display)


class StrikerEnemy(IEnemy):
    _speed = 1
    MAX_HP = 150
    HP = MAX_HP

    def __init__(self, images: list, pos: list, factory, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, factory, *groups, **kwargs)
        self.movement = StaticMovement(pg.Vector2(-1, 0))
        self.healthbar = HealthBar((self.rect.left, self.rect.top + int(self.rect.height*.22)),
                                   self.HP, self.MAX_HP, (self.rect.width, int(self.rect.height*.11)))

    def updatePosition(self, *args, **kwargs):
        self.movement.update(self.rect, self.rects, speed=self._speed)

        if self.rect.left <= 0:
            self.movement.changeDirection(update_x=1)
        elif self.rect.right >= kwargs.get('display_size')[0]:
            self.movement.changeDirection(update_x=-1)

        return super().updatePosition(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.healthbar.updateHP(self.HP)
        self.healthbar.update(
            self.rect.left, self.rect.top - int(self.rect.height*.22))
        return super().update(*args, **kwargs)

    def draw(self, display):
        self.healthbar.draw(display)
        return super().draw(display)

# ---------------------------FACTORIES--------------------------------------


class AbstarctFactory:
    object = None

    def __init__(self, display_size, group=None, *args, **kwargs):
        self.information = FactoryInformation()
        self.display_size = display_size
        self.group = group

        self.particle_group = kwargs.get('particle_group')

    def createObject(self, amount=1, *args, **kwargs):
        """create and add object to group"""
        self.information.spawned += amount
        self.information.alive += amount

    def count(self):
        return self.information.alive

    def updateAllObjectCondition(self, func):
        """apply fuction to all gropu object 
        for example, change damage
        """
        pass

    def spriteWasKilled(self, instance=None):
        self.information.killed += 1
        self.information.alive -= 1

    def spriteWasDestroy(self, instance=None):
        self.information.alive -= 1

    def __destroyAllObject(self):
        pass


# ------------------------------------------------------------------


class AsteroidFactory(AbstarctFactory):
    object = Asteroid

    def __init__(self, display_size, group=None,  *args, **kwargs):
        super().__init__(display_size, group=group, *args, **kwargs)
        self.all_images = [pg.image.load(
            IMAGES+'\enemy\\asteroid\\asteroid'+str(i)+'.png').convert_alpha() for i in range(1, 7)]
        self.burst_images = [pg.image.load(
            IMAGES+'\enemy\\asteroid\\burst\\asteroid'+str(i)+'.png').convert_alpha() for i in range(1, 5)]

    def createObject(self, *args, **kwargs):
        random_image = random.choice(self.all_images)
        spawn_pos = (random.randint(
            10, self.display_size[0]), -random_image.get_rect().height)
        _obj = self.object([random_image], spawn_pos, self,
                           self.group, burst_images=self.burst_images)
        return super().createObject(amount=1, *args, **kwargs)


class FirstFlightEnemyFactory(AbstarctFactory):
    object = FirstFlightEnemy2

    def __init__(self, display_size, group=None, *args, **kwargs):
        super().__init__(display_size, group=group, *args, **kwargs)
        self.images = [pg.image.load(
            IMAGES+'\enemy\\firstFlight\\1Enemy'+str(i)+'.png').convert_alpha() for i in range(1, 3)]
        self.burst_images = [pg.image.load(
            IMAGES+'\enemy\\firstFlight\\burst\\1Enemy'+str(i)+'.png').convert_alpha() for i in range(1, 10)]

    def createObject(self, *args, **kwargs):
        _obj = self.object(
            self.images, (-self.display_size[0]*0.1, self.display_size[1]*0.2), self, self.group, particle_group=self.particle_group, burst_images=self.burst_images)
        return super().createObject(amount=1, *args, **kwargs)


class StarEnemyFactory(AbstarctFactory):
    object = StarEnemy

    def __init__(self, display_size, group=None, *args, **kwargs):
        super().__init__(display_size, group=group, *args, **kwargs)
        self.images = [pg.image.load(
            IMAGES+'\enemy\\star\\star1.png').convert_alpha()]

    def createObject(self, *args, **kwargs):
        _obj_width, _obj_height = self.images[0].get_width(
        ), self.images[0].get_height()

        pos = [random.randint(_obj_width, self.display_size[0]-_obj_height),
               random.randint(_obj_height, self.display_size[1] - _obj_height)]

        _obj = self.object(
            self.images, pos, self, self.group, particle_group=self.particle_group)
        return super().createObject(amount=1, *args, **kwargs)


class StrikerEnemyFactory(AbstarctFactory):
    object = StrikerEnemy

    def __init__(self, display_size, group=None, *args, **kwargs):
        super().__init__(display_size, group, *args, **kwargs)
        self.images = [pg.image.load(
            IMAGES+'\enemy\\striker\\strikerEnemy1.png').convert_alpha()]

    def createObject(self, amount=1, *args, **kwargs):
        pos = (self.display_size[0]-self.images[0].get_width()-3,
               int(self.images[0].get_height()*1.5))
        self.object(
            self.images, pos, self, self.group)
        return super().createObject(amount, *args, **kwargs)


class FactoryInformation:
    killed: int = 0
    alive: int = 0
    spawned: int = 0
