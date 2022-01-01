import pygame as pg
from pygame.sprite import Sprite, AbstractGroup, Group
from settings import IMAGES
import random


class AbstaractBackground:

    def __init__(self, mediator, size, group, *args, **kwargs):
        self.aplication = mediator
        self.size = size
        self.group = group

    def update(self, *args, **kwargs):
        """update background and background pieces"""

    def draw(self, display, *args, **kwargs):
        """draw background and background pieces"""

    @classmethod
    def randomPos(self, display_size):
        return (random.randint(0, display_size[0]), random.randint(0, display_size[1]))


class StarsBackground(AbstaractBackground):
    def __init__(self, mediator, size: tuple, group, stars_amount=20, particle_amount=40, *args, **kwargs):
        super().__init__(mediator, size, group, *args, **kwargs)

        self.direction = pg.Vector2(0, 1)
        self.speed = 1

        self.stars_images = [pg.image.load(
            IMAGES + f'\\background\\star{i}.png') for i in range(1, 3)]

        for i in range(particle_amount):
            self.group.add(BackgroundParticle(
                self.randomPos(self.size), self.direction, self.speed))

        for j in range(stars_amount):
            self.group.add(ImageBackgroundParticle(self.randomPos(
                self.size), self.direction, self.speed, [random.choice(self.stars_images)]))


class BackgroundParticle(Sprite):
    def __init__(self, center: list, direction, speed, *groups: AbstractGroup, **kwargs):
        super().__init__(*groups)
        self.size = kwargs.get('size') if kwargs.get(
            'size') else random.randint(2, 5)
        self.image = pg.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=center)
        self.direction = direction
        self.speed = speed

    def update(self, *args, **kwargs):
        # self.rect.centerx += self.direction.x * self.speed
        # self.rect.centery += self.direction.y * self.speed
        pass

    def draw(self, display):
        display.blit(self.image, self.rect)


class ImageBackgroundParticle(BackgroundParticle):
    def __init__(self, center: list, direction, speed, images: list, *groups: AbstractGroup, **kwargs):
        super().__init__(center, direction, speed, *groups, **kwargs)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=center)
