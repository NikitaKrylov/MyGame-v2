import pygame
from pygame.sprite import Sprite, AbstractGroup
from animation import Animator
from animation import StaticMovement, Animator
import random


class Particle(Sprite):
    def __init__(self, pos, size, speed, color: list, vector, life_size=None,  size_rate=None, life_time=None, *groups: AbstractGroup):
        super().__init__(*groups)
        self.life_size = life_size
        self.size_rate = size_rate
        self.life_time = life_time
        self.direction = vector
        self.size = size
        self.speed = speed
        self.image = pygame.Surface((self.size, self.size))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args, **kwargs):
        self.size += self.size_rate
        self.speed -= 0.3

        if self.speed <= 0:
            self.kill()

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.life_size:
            if self.life_size > self.size:
                self.kill()

        return super().update(*args, **kwargs)
    


class BaseShell(Sprite):
    isPlayer: bool = None
    animation = Animator

    def __init__(self, images: list,  pos, particle_group, *groups: AbstractGroup):
        super().__init__(*groups)
        self.particle_group = particle_group
        self.animation = self.animation()
        self.DAMAGE = 10
        self.speed = 25
        self.images = images
        self.image = images[0]
        self.movement = StaticMovement(pygame.Vector2(0.0, -1.0))
        """Изображение, которое должно рисоваться в данный момент,
        должно быть названо image для нормально работы группы
        """
        self.rect = self.image.get_rect(center=pos)
        self.rects = [self.rect]

    def update(self, *args, **kwargs):
        self.rect, self.rects = self.movement.update(
            self.rect,
            self.rects,
            speed=self.speed
        )

        if self.rect.bottom < -self.rect.bottom:
            super().kill()

        return super().update(*args, **kwargs)

    def getDamage(self):
        damage = self.DAMAGE
        self.kill()
        return damage

    def kill(self):
        return super().kill()


class FirstShell(BaseShell):
    def __init__(self, images: list, pos, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.rects = [pygame.Rect(self.rect.x + self.rect.width * 0.15, self.rect.y +
                                  self.rect.height * 0.15, self.rect.width*0.7, self.rect.height*0.7)]
        self.DAMAGE = 25
        self.speed = 23

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
                size_rate=-0.5))
        return super().kill()


class SecondShell(BaseShell):
    def __init__(self, images: list, pos, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.rects = [pygame.Rect(self.rect.x + self.rect.width * 0.3, self.rect.y +
                                  self.rect.height * 0.3, self.rect.width*0.6, self.rect.height*0.6)]
        self.DAMAGE = 17
        self.speed = 19

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
                size_rate=-0.5))
        return super().kill()

