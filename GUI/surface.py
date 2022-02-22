import pygame as pg
from pygame.sprite import Sprite
from pygame import gfxdraw
from pygame.font import Font
from logger import get_logger
log = get_logger(__name__)

# This class is used to create text objects that can be drawn to the screen
class Text(Sprite):
    def __init__(self, pos: list, text: str, color: list, font: Font, center: bool = False):
        super().__init__()
        self.text = text
        self.color = color
        self.font = font
        self.center = center

        self.textsurface = self.font.render(self.text, False, self.color)
        self.rect = self.textsurface.get_rect(topleft=pos)
        if center:
            self.rect.center = pos

    def draw(self, display):
        display.blit(self.textsurface, self.rect)

    def update(self, *args, **kwargs):
        _text = kwargs.get('text')
        if _text:
            if self.text != _text:
                self.text = _text
                self.textsurface = self.font.render(
                    self.text, False, self.color)

    def updateText(self, text: str):
        if not isinstance(text, str):
            return log.error("text to render must be string")

        self.text = text
        self.textsurface = self.font.render(self.text, False, self.color)

        if self.center:
            self.rect = self.textsurface.get_rect(center=self.rect.center)
        else:
            self.rect = self.textsurface.get_rect(topleft=self.rect.topleft)

# The base surface class is the parent class of all other surface classes
class BaseSurface(Sprite):
    def __init__(self, pos: list, size: list = None, center: bool = False, **kwargs):
        super().__init__()
        self.pos = pos
        self.size = size
        self.kwargs: dict = kwargs
        self.isHover = False

    def draw(self, display):
        pass

    @classmethod
    def scale(self, image,  scale_value):
        width, height = image.get_width(), image.get_height()
        return pg.transform.scale(image, (int(width*scale_value), int(height*scale_value)))

# The class creates a surface with a color
class ColoredSurface(BaseSurface):
    def __init__(self, pos: list, size: list, center: bool = False, color=None, border_radius=0,  **kwargs):
        super().__init__(pos, size, center,  **kwargs)
        self.border_radius = border_radius
        self.color = color
        self.image = pg.Surface(self.size)

        if self.color is not None:
            self.image.fill(self.color)

        if center:
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, display):
        # pg.draw.rect(display, self.color, self.rect,
        #              border_radius=self.border_radius)
        gfxdraw.box(display, self.rect, self.color)
        return super().draw(display)


# The ImageSurface class is a surface that is created from an image
class ImageSurface(BaseSurface):
    def __init__(self, pos: list,  image, size: list = None, center: bool = False,  **kwargs):
        super().__init__(pos, size, center,  **kwargs)
        self.image = image

        if center:
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)

    def draw(self, display):
        display.blit(self.image, self.rect)
        return super().draw(display)


# A toggle button that can be toggled on and off
class ToggleButton(ImageSurface):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, onClickImage=None, **kwargs):
        super().__init__(pos, image, size, center, func, **kwargs)
        self.state = False

        self.onClickImage = onClickImage if onClickImage is not None else self.image
        self.defaultImage = self.image

    def update(self, *args, **kwargs):
        self.rect = self.image.get_rect(center=self.rect.center)
        return super().update(*args, **kwargs)

    def execute(self):
        self.state = not self.state

        if self.state:
            self.image = self.onClickImage
        else:
            self.image = self.defaultImage

        self.rect = self.image.get_rect(center=self.rect.center)

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


# This class is a subclass of the ToggleButton class. 
# It has the same parameters as the ToggleButton class, 
# but it also has a font parameter.
class TextToggleButton(ToggleButton):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, onClickImage=None, font=None, **kwargs):
        super().__init__(pos, image, size, center, func, onClickImage, **kwargs)
        self.font = font

    def changeImage(self, image=None, text=None):
        if image or text:
            if text:
                self.image = self.font.render(text, False, (255, 255, 255))
            if image:
                self.image = image

            self.onClickImage = self.image
            self.defaultImage = self.image
