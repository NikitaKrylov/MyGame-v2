from logger import get_logger
from .surface import ColoredSurface, ImageSurface
import pygame as pg

log = get_logger(__name__)


def hasattribute(name: str = None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if name is not None:
                if not hasattr(self, name):
                    log.error(
                        f"'{self.__class__.__name__}' object has no attribute {name}")
                    return
            try:
                result = func(self, *args, **kwargs)
            except AttributeError as exp:
                log.error(exp)
            else:
                return result
        return wrapper
    return decorator


class IButton:
    def execute(self):
        if self.func is not None:
            self.func()


class IHoveredButton(IButton):

    @staticmethod
    def draw(self, display):
        if not hasattr(self, "isHover"):
            log.error("self object has not an atribute 'isHover' ")
            return

        elif not hasattr(self, "scaled_surface"):
            log.error("self object has not an atribute 'scaled_surface' ")
            return

        if self.isHover:
            self.rect = self.scaled_surface.get_rect(center=self.rect.center)
            display.blit(self.scaled_surface, self.rect)
        else:
            self.rect = self.surface.get_rect(center=self.rect.center)
            display.blit(self.surface, self.rect)


class ColoredButton(ColoredSurface, IHoveredButton):
    pass


class ImageButton(ImageSurface, IHoveredButton):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, **kwargs):
        super().__init__(pos, image, size, center, func, **kwargs)
        self.scaled_surface = self.scale(self.surface, 1.1)

    def draw(self, display):
        return IHoveredButton.draw(self, display)


class ToggleButton(ImageSurface, IButton):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, onClickImage=None, **kwargs):
        super().__init__(pos, image, size, center, func, **kwargs)
        self.state = False

        if onClickImage:
            self.onClickImage = onClickImage
        else:
            self.onClickImage = None

        self.defaultImage = self.surface

    def update(self, *args, **kwargs):
        self.rect = self.surface.get_rect(center=self.rect.center)
        return super().update(*args, **kwargs)

    def execute(self):
        self.state = not self.state

        if self.state:
            self.surface = self.onClickImage
        else:
            self.surface = self.defaultImage

        self.rect = self.surface.get_rect(center=self.rect.center)

        return super().execute()

    def draw(self, display):
        padding = 10
        if self.isHover:
            pg.draw.lines(display, (255, 255, 255), True, (
                (self.rect.left-padding, self.rect.top-padding),
                (self.rect.right+padding, self.rect.top-padding),
                (self.rect.right+padding, self.rect.bottom+padding),
                (self.rect.left-padding, self.rect.bottom+padding)
            ), width=3)

        return super().draw(display)


class TextToggleButton(ToggleButton):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, onClickImage=None, font=None, **kwargs):
        super().__init__(pos, image, size, center, func, onClickImage, **kwargs)
        self.font = font

    def changeImage(self, image=None, text=None):
        if image or text:
            if text:
                self.surface = self.font.render(text, False, (255, 255, 255))
            if image:
                self.surface = image

            self.onClickImage = self.surface
            self.defaultImage = self.surface
