import pygame as pg
from pygame.sprite import Sprite
from pygame import gfxdraw


class Text(Sprite):
    def __init__(self, pos:list, text: str, font_size: int, color: list, center: bool = False, font_name: str = None, font_path: str = None, font_object:pg.font.Font=None, bold=False, italic=False):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.color = color

        if font_name is not None:
            self.font = pg.font.SysFont(
                font_name, self.font_size, italic=italic, bold=bold)
        elif font_path is not None:
            pass
        elif isinstance(font_object, pg.font.Font):
            self.font = font_object

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


class BaseSurface(Sprite):
    def __init__(self, pos: list, size: list = None, center: bool = False, func=None, **kwargs):
        super().__init__()
        self.pos = pos
        self.size = size
        self.kwargs: dict = kwargs
        self.func = func
        self.isHover = False

    def draw(self, display):
        pass

    @classmethod
    def scale(self, surface,  scale_value):
        width, height = surface.get_width(), surface.get_height()
        return pg.transform.scale(surface, (int(width*scale_value), int(height*scale_value)))


class ColoredSurface(BaseSurface):
    def __init__(self, pos: list, size: list, center: bool = False, color=None, border_radius=0, func=None, **kwargs):
        super().__init__(pos, size, center, func=func, **kwargs)
        self.border_radius = border_radius
        self.color = color
        self.surface = pg.Surface(self.size)

        if self.color is not None:
            self.surface.fill(self.color)

        if center:
            self.rect = self.surface.get_rect(center=self.pos)
        else:
            self.rect = self.surface.get_rect(topleft=self.pos)

    def draw(self, display):
        # pg.draw.rect(display, self.color, self.rect,
        #              border_radius=self.border_radius)
        gfxdraw.box(display, self.rect, self.color)
        return super().draw(display)


class ImageSurface(BaseSurface):
    def __init__(self, pos: list,  image, size: list = None, center: bool = False, func=None, **kwargs):
        super().__init__(pos, size, center, func=func, **kwargs)
        self.surface = image

        if center:
            self.rect = self.surface.get_rect(center=self.pos)
        else:
            self.rect = self.surface.get_rect(topleft=pos)

    def draw(self, display):
        display.blit(self.surface, self.rect)
        return super().draw(display)


# class ColoredButton(ColoredSurface):
#     def __init__(self, pos: list, size: list, center: bool = False, color=None, border_radius=0, func=None, **kwargs):
#         super().__init__(pos, size, center=center, color=color,
#                          border_radius=border_radius, func=func, **kwargs)


# class ImageButton(ImageSurface):
#     def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, **kwargs):
#         super().__init__(pos, image, size=size, center=center, func=func, **kwargs)
#         self.scaled_surface = self.scale(self.surface, 1.1)

#     def draw(self, display):
#         if self.isHover:
#             self.rect = self.scaled_surface.get_rect(center=self.rect.center)
#             display.blit(self.scaled_surface, self.rect)
#         else:
#             self.rect = self.surface.get_rect(center=self.rect.center)
#             display.blit(self.surface, self.rect)

#         return


class ToggleButton(ImageSurface):
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
