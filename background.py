from turtle import Vec2D
import pygame as pg
from pygame.sprite import Sprite, AbstractGroup, Group
from changed_group import CustomGroup
from settings import IMAGES
import random
from logger import get_logger
log = get_logger(__name__)


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

# ------------------------------------------------------------------------------------------------------


class IBackgroundComponent(Sprite):
    def __init__(self, display_size, *groups: AbstractGroup):
        super().__init__(*groups)
        self.group = CustomGroup()
        self.display_size = display_size

    def Start(self):
        """create background components and put into group
        """

    def kill(self):
        self.group.empty()

    def update(self, *args, **kwargs):
        self.group.update(*args, **kwargs)

    def draw(self, display):
        self.group.draw(display)

    @classmethod
    def randomPos(self, size: list):
        x = random.randint(min(0, size[0]), max(0, size[0]))
        y = random.randint(min(0, size[1]), max(0, size[1]))

        return [x, y]


class ParticleStarComponent(IBackgroundComponent):
    prefab = BackgroundParticle

    def __init__(self, display_size, amount=20, speed=1, *groups: AbstractGroup):
        super().__init__(display_size, *groups)
        self.amount = amount
        self.speed = speed

    def update(self, *args, **kwargs):
        if len(self.group.sprites()) < self.amount * 2:
            self._createPreviousScene()

        return super().update(*args, **kwargs)

    def Start(self):
        for i in range(self.amount):
            self._createScene()

        for i in range(self.amount):
            self._createPreviousScene()

    def _createScene(self):
        self.__class__.prefab(
            self.__class__.randomPos(self.display_size), pg.Vector2(0, 1), self.speed, self.group)

    def _createPreviousScene(self):
        self.__class__.prefab(
            self.__class__.randomPos([self.display_size[0], -self.display_size[1]]), pg.Vector2(0, 1), self.speed, self.group)

        return super().Start()


class ImageStarComponent(ParticleStarComponent):
    prefab = ImageBackgroundParticle

    def __init__(self, display_size, amount=20, speed=1, *groups: AbstractGroup):
        super().__init__(display_size, amount, speed, *groups)
        self.images = [pg.image.load(
            IMAGES + f'\\background\\star{i}.png') for i in range(1, 3)]

    def _createScene(self):
        self.__class__.prefab(
            self.__class__.randomPos(self.display_size), pg.Vector2(0, 1), self.speed, [random.choice(self.images)], self.group)

    def _createPreviousScene(self):
        self.__class__.prefab(
            self.__class__.randomPos([self.display_size[0], -self.display_size[1]]), pg.Vector2(0, 1), self.speed, [random.choice(self.images)], self.group)


# ------------------------------------------------------------------------------------------------------

class BackgroundSurface(Sprite):
    def __init__(self, topleft, image, speed, direction=pg.Vector2(0, 1), *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        self.speed = speed
        self.direction = direction

    def update(self, *args, **kwargs):
        self.rect.topleft += self.direction * self.speed
        return super().update(*args, **kwargs)

    def draw(self, display):
        display.blit(self.image, self.rect)


class SurfaceComponent(IBackgroundComponent):
    prefab = BackgroundSurface
    color = (2, 4, 5)

    def __init__(self, display_size, speed, *groups: AbstractGroup):
        super().__init__(display_size, *groups)
        self.speed = speed

    def Start(self):
        self._createScene()
        self._createPreviousScene()
        return super().Start()

    def _createScene(self):
        image = pg.Surface(self.display_size)
        image.fill(self.__class__.color)
        self.__class__.prefab((0, 0), image, self.speed,
                              pg.Vector2(0, 1), self.group)

    def _createPreviousScene(self):
        image = pg.Surface(self.display_size)
        image.fill(self.__class__.color)
        self.__class__.prefab(
            (0, -self.display_size[1]), image, self.speed, pg.Vector2(0, 1), self.group)

    def update(self, *args, **kwargs):
        sprite_list = self.group.sprites()

        for sprite in sprite_list:
            if sprite.rect.top > self.display_size[1]:
                if sprite_list.index(sprite) == len(sprite_list)-1:
                    sprite.rect.bottom = sprite_list[0].rect.top
                elif sprite_list.index(sprite) == 0:
                    sprite.rect.bottom = sprite_list[len(
                        sprite_list)-1].rect.top

        return super().update(*args, **kwargs)


# ------------------------------------------------------------------------------------------------------


class BackgroundManager:
    surface = SurfaceComponent

    def __init__(self,  display_size, group: AbstractGroup):
        self.display_size = display_size
        self.BackgroundGroup = group
        self.speed = 2

        self.surfaceComponent = self.surface(
            self.display_size, self.speed, self.BackgroundGroup)

        self.starsCompontnt = ParticleStarComponent(
            self.display_size, 20, self.speed, self.BackgroundGroup)
        self.starsImageCompontnt = ImageStarComponent(
            self.display_size, 10, self.speed, self.BackgroundGroup)

        self.surfaceComponent.Start()
        self.starsCompontnt.Start()
        self.starsImageCompontnt.Start()

    def update(self, **kwargs):
        pass
