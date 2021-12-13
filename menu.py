import pygame as pg
from pygame.sprite import Sprite


class BaseText:
    def __init__(self, text: str, font_size: int, color: list, center: bool = False, font=None, font_path=None):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = font

    def draw(self, display):
        pass


class BaseSurface(Sprite):
    def __init__(self, pos: list, size: list = None, center: bool = False,  **kwargs):
        super().__init__()
        self.pos = pos
        self.size = size
        self.kwargs: dict = kwargs

    def draw(self, display):
        pass


class ColoredSurface(BaseSurface):
    def __init__(self, pos: list, size: list, center: bool = False, color=None, border_radius=0, **kwargs):
        super().__init__(pos, size, center, **kwargs)
        self.border_radius = border_radius
        self.color = color
        self.surface = pg.Surface(self.size)

        if center:
            self.rect = self.surface.get_rect(center=self.pos)
        else:
            self.rect = self.surface.get_rect(topleft=self.pos)

    def draw(self, display):
        pg.draw.rect(display, self.color, self.rect,
                     border_radius=self.border_radius)
        return super().draw(display)


class ImageSurface(BaseSurface):
    def __init__(self, pos: list,  image, size: list = None, center: bool = False, **kwargs):
        super().__init__(pos, size, center, **kwargs)
        self.image = image

        if center:
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)

    def draw(self, display):
        display.blit(self.image, self.rect)
        return super().draw(display)


class ColoredButton(ColoredSurface):
    def __init__(self, pos: list, size: list, center: bool = False, color=None, border_radius=0, **kwargs):
        super().__init__(pos, size, center=center, color=color,
                         border_radius=border_radius, **kwargs)


class ImageButton(ImageSurface):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, **kwargs):
        super().__init__(pos, image, size=size, center=center, **kwargs)
