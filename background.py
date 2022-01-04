import pygame as pg
from pygame.sprite import Sprite, AbstractGroup, Group
from settings import IMAGES
import random


class AbstaractBackground:

    def __init__(self, mediator, size, group, *args, **kwargs):
        self.aplication = mediator
        self.size = size
        self.group = group
        self.counter = 0
        # self.eventupdateNumber = pg.USEREVENT + 1
        # delay = 60
        # pg.time.set_timer(self.eventupdateNumber, delay)

    def update(self, *args, **kwargs):
        """update background and background pieces"""

    def draw(self, display, *args, **kwargs):
        """draw background and background pieces"""

    @classmethod
    def randomPos(self, size):
        width = random.randint(
            0, size[0]) if size[0] > 0 else random.randint(size[0], 0)
        height = random.randint(
            0, size[1]) if size[1] > 0 else random.randint(size[1], 0)

        return [width, height]


class StarsBackground(AbstaractBackground):
    scene_speed = 1
    element_speed = scene_speed

    def __init__(self, mediator, size: tuple, group, stars_amount=20, particle_amount=40, *args, **kwargs):
        super().__init__(mediator, size, group, *args, **kwargs)

        self.stars_amount = stars_amount
        self.particle_amount = particle_amount

        self.direction = pg.Vector2(0, 1)
        self.stars_images = [pg.image.load(
            IMAGES + f'\\background\\star{i}.png') for i in range(1, 3)]

        self.createScene(self.size, stars_amount, particle_amount)
        self.createScene([self.size[0], -self.size[1]],
                         stars_amount, particle_amount)

    # @property
    # def element_speed(self):
    #     return random.randint(1, 2)

    def createScene(self, size, stars_amount, particle_amount):
        for i in range(particle_amount):
            self.group.add(BackgroundParticle(
                self.randomPos(size), self.direction, self.element_speed))

        for j in range(stars_amount):
            self.group.add(ImageBackgroundParticle(self.randomPos(
                size), self.direction, self.element_speed, [random.choice(self.stars_images)]))

    def update(self, *args, **kwargs):
        self.counter += self.scene_speed

        if self.counter >= self.size[1]:
            self.createScene([self.size[0], -self.size[1]],
                             self.stars_amount, self.particle_amount)
            self.counter = 0

        return super().update(*args, **kwargs)


class FustStarsBackground(StarsBackground):
    scene_speed = 4
    element_speed = scene_speed


# Background pieces


class BackgroundParticle(Sprite):
    def __init__(self, center: list, direction, speed, *groups: AbstractGroup, **kwargs):
        super().__init__(*groups)
        self.size = kwargs.get('size') if kwargs.get(
            'size') else random.randint(1, 3)
        self.image = pg.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=center)
        self.direction = direction
        self.speed = random.choice(speed) if isinstance(
            speed, (list, tuple)) else speed
    

    def update(self, *args, **kwargs):
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

        if self.rect.top > kwargs.get('display_size')[1]:
            self.kill()

        return super().update(*args, **kwargs)

    def draw(self, display):
        display.blit(self.image, self.rect)


class ImageBackgroundParticle(BackgroundParticle):
    def __init__(self, center: list, direction, speed, images: list, *groups: AbstractGroup, **kwargs):
        super().__init__(center, direction, speed, *groups, **kwargs)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=center)
