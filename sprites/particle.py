import pygame
from pygame.sprite import Sprite, AbstractGroup
from animation import Animator
from animation import StaticMovement, Animator
import random

# A particle is a sprite that has a size, a speed, a color, and a direction.
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



# This is a particle that deals damage to the player
class ParticleShell(Particle):
    def __init__(self, pos, size, speed, color: list, vector, damage, life_size=None, size_rate=None, speed_rate=None, life_time=None, shape='square', *groups: AbstractGroup, **kwargs):
        super().__init__(pos, size, speed, color, vector, life_size=life_size,
                         size_rate=size_rate, speed_rate=speed_rate, life_time=life_time, shape=shape, *groups, **kwargs)
        self.DAMAGE = damage
        self.rects = [self.rect]

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.rects = [self.rect]

    def getDamage(self):
        damage = self.DAMAGE
        self.kill()
        return damage