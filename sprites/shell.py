from math import sin
import pygame
from pygame.sprite import Sprite, AbstractGroup
from animation import Animator
from animation import StaticMovement, Animator
import random


# ----------------------------------PARTICLES---------------------------------------------

class Particle(Sprite):
    def __init__(self, pos, size, speed, color: list, vector, life_size=None,  size_rate=None, speed_rate=None, life_time=None, shape='square', *groups: AbstractGroup):
        super().__init__(*groups)
        self.life_size = life_size
        self.size_rate = size_rate
        self.life_time = life_time
        self.direction = vector
        self.size = size
        self.speed_rate = speed_rate
        self.shape = shape
        self.speed = speed
        self.image = pygame.Surface((self.size, self.size))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args, **kwargs):
        self.size += self.size_rate

        if self.speed_rate:
            self.speed += self.speed_rate

            if self.speed <= 0:
                self.kill()

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.life_size:
            if self.size_rate < 0 and self.life_size > self.size:
                self.kill()
            elif self.size_rate > 0 and self.life_size <= self.size:
                self.kill()

        return super().update(*args, **kwargs)

    def draw(self, display):
        if self.shape == 'square':
            display.blit(self.image, self.rect)
        elif self.shape == 'circle':
            pygame.draw.circle(display, self.color,
                               self.rect.center, self.size//2)


class ParticleShell(Particle):
    def __init__(self, pos, size, speed, color: list, vector, damage, life_size=None, size_rate=None, speed_rate=None, life_time=None, shape='square', *groups: AbstractGroup, **kwargs):
        super().__init__(pos, size, speed, color, vector, life_size=life_size,
                         size_rate=size_rate, speed_rate=speed_rate, life_time=life_time, shape=shape, *groups, **kwargs)
        self._damage = damage
        self.rects = [self.rect]

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.rects = [self.rect]

    def getDamage(self):
        damage = self._damage
        self.kill()
        return damage


# ----------------------------------BASE SHELL---------------------------------------------


class BaseShell(Sprite):
    isPlayer: bool = None
    animation = Animator
    _damage = 10
    _speed = 20

    def __init__(self, images: list,  pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(*groups)
        self.particle_group = particle_group
        self.animation = self.animation()
        self.images = images
        self.image = images[0]
        self.movement = StaticMovement(pygame.Vector2(0.0, -1.0))
        """Изображение, которое должно рисоваться в данный момент,
        должно быть названо image для нормально работы группы
        """
        self.rect = self.image.get_rect(center=pos)
        self.rects = [self.rect]

    def update(self, *args, **kwargs):
        self.movement.update(
            self.rect,
            self.rects,
            speed=self._speed
        )

        if self.rect.bottom < -self.rect.bottom:
            super().kill()
        elif self.rect.top > kwargs.get('display_size')[1]:
            super().kill()

        return super().update(*args, **kwargs)

    def getDamage(self):
        damage = self._damage
        self.kill()
        return damage

    def draw(self, display):
        return display.blit(self.image, self.rect)

    def kill(self):
        return super().kill()


# ----------------------------------PLAYER SHELL---------------------------------------------


class FirstShell(BaseShell):
    _damage = 25
    _speed = 20

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.rects = [pygame.Rect(self.rect.x + self.rect.width * 0.15, self.rect.y +
                                  self.rect.height * 0.15, self.rect.width*0.7, self.rect.height*0.7)]

    def kill(self):
        """create particles when sprite die"""
        colors = [(170, 238, 255), (127, 233, 247), (180, 248, 255)]
        for i in range(9):
            vector = pygame.Vector2(1, 0).rotate(random.randint(1, 359))
            self.particle_group.add(Particle(
                pos=self.rect.center,
                size=random.randint(6, int(self.rect.width/2)),
                speed=random.randint(8, 12),
                color=random.choice(colors),
                vector=vector,
                life_size=5,
                speed_rate=-0.3,
                size_rate=-0.5))
        return super().kill()


class RedShell(BaseShell):
    _damage = 17
    _speed = 19

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.rects = [pygame.Rect(self.rect.x + self.rect.width * 0.3, self.rect.y +
                                  self.rect.height * 0.3, self.rect.width*0.6, self.rect.height*0.6)]

    def kill(self):
        """create particles when sprite die"""
        colors = [(200, 20, 20), (180, 11, 11), (200, 0, 0)]
        for i in range(7):
            vector = pygame.Vector2(1, 0).rotate(random.randint(1, 359))
            self.particle_group.add(Particle(
                pos=self.rect.center,
                size=random.randint(6, self.rect.width//2.5),
                speed=random.randint(6, 10),
                color=random.choice(colors),
                vector=vector,
                life_size=5,
                speed_rate=-0.3,
                size_rate=-0.5))
        return super().kill()


class Rocket(BaseShell):
    _speed = 5
    _damage = 120

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)

    def update(self, *args, **kwargs):
        colors = [(190, 192, 194), (164, 165, 166),
                  (206, 206, 214), (129, 129, 130)]
        for i in range(2):
            vector = pygame.Vector2(0, -1).rotate(random.randint(-20, 20))
            self.particle_group.add(Particle(
                pos=[self.rect.centerx, self.rect.bottom],
                size=random.randint(6, self.rect.width//2.5),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=vector,
                life_size=random.randint(18, 30),
                size_rate=random.uniform(0.35, 0.6),
                speed_rate=-0.3,
                shape='circle'))
        return super().update(*args, **kwargs)

    def kill(self):
        colors = [(255, 0, 0), (255, 140, 0), (255, 90, 0)]
        for i in range(70):
            vector = pygame.Vector2(0, -1).rotate(random.randint(-20, 20))
            self.particle_group.add(Particle(
                pos=[random.randint(self.rect.left-self.rect.width//2, self.rect.right+self.rect.width//2), random.randint(
                    self.rect.top - self.rect.height//2, self.rect.bottom + self.rect.height//2)],
                size=random.randint(2, self.rect.width//2),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=vector,
                life_size=random.randint(50, 100),
                size_rate=random.uniform(2, 5),
                speed_rate=-.3,
                shape='circle'))

        return super().kill()


class BurnedShell(BaseShell):
    _speed = 13
    _damage = 15
    PARTICLE_DAMAGE = 7

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)

        self.rects = [pygame.Rect(self.rect.x + self.rect.width * 0.375, self.rect.y +
                                  self.rect.height * 0.375, self.rect.width*0.25, self.rect.height*0.25)]

    def kill(self):
        colors = [(255, 0, 0), (255, 140, 0), (255, 90, 0)]
        group = self.groups()[0]

        for i in range(random.randint(4, 7)):
            group.add(ParticleShell(
                pos=self.rect.center,
                size=self.rect.width//5,
                speed=random.randint(12, 16),
                color=random.choice(colors),
                vector=pygame.Vector2(1, 0).rotate(random.randint(1, 359)),
                damage=self.PARTICLE_DAMAGE,
                life_size=2,
                size_rate=-0.4,
                speed_rate=-0.3,
                shape='square'
            ))
        return super().kill()


# ----------------------------------ENEMT SHELL---------------------------------------------


class RedEnemyShell(RedShell):
    _damage = 2
    _speed = 10

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.movement.changeDirection(update_y=1)

    def damage(self, value):
        return super().kill()


class StarEnemyShell(BaseShell):
    _speed = 3
    _damage = 5

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        vector = kwargs.get('vector')
        self.movement.changeDirection(update_y=vector.y)
        self.movement.changeDirection(update_x=vector.x)

    def kill(self):
        colors = ["#8cd7fb", "#71c9f2", "#bfe9fd"]
        for i in range(4):
            self.particle_group.add(Particle(
                pos=self.rect.center,
                size=int(self.rect.width*0.7),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=pygame.Vector2(1, 0).rotate(random.randint(1, 359)),
                life_size=random.randint(2, 4),
                size_rate=-random.uniform(0.5, 0.6),
                speed_rate=-0.3,
                shape='square'))

        return super().kill()

    def damage(self, value):
        return self.kill()
