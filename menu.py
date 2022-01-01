import pygame as pg
from pygame.sprite import Sprite, spritecollide
from settings import IMAGES
from pygame.sprite import Group
from changed_group import CustomGroup


class Text:
    def __init__(self, pos, text: str, font_size: int, color: list, center: bool = False, font_name=None, font_path=None, bold=False, italic=False):
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.color = color

        if font_name:
            self.font = pg.font.SysFont(
                font_name, self.font_size, italic=italic, bold=bold)
        elif font_path:
            pass

        self.textsurface = self.font.render(self.text, False, self.color)

        if center:
            self.pos[0] -= self.textsurface.get_width()//2

    def draw(self, display):
        display.blit(self.textsurface, self.pos)


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

    def execute(self):
        if self.func:
            self.func()

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

        if center:
            self.rect = self.surface.get_rect(center=self.pos)
        else:
            self.rect = self.surface.get_rect(topleft=self.pos)

    def draw(self, display):
        pg.draw.rect(display, self.color, self.rect,
                     border_radius=self.border_radius)
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


class ColoredButton(ColoredSurface):
    def __init__(self, pos: list, size: list, center: bool = False, color=None, border_radius=0, func=None, **kwargs):
        super().__init__(pos, size, center=center, color=color,
                         border_radius=border_radius, func=func, **kwargs)


class ImageButton(ImageSurface):
    def __init__(self, pos: list, image, size: list = None, center: bool = False, func=None, **kwargs):
        super().__init__(pos, image, size=size, center=center, func=func, **kwargs)
        self.scaled_surface = self.scale(self.surface, 1.1)

    def draw(self, display):
        if self.isHover:
            self.rect = self.scaled_surface.get_rect(center=self.rect.center)
            display.blit(self.scaled_surface, self.rect)
        else:
            self.rect = self.surface.get_rect(center=self.rect.center)
            display.blit(self.surface, self.rect)

        return


class Menu:
    def __init__(self, mediator, display_size):
        self.aplication = mediator
        self.display_size = (self.width, self.height) = display_size
        
        blured_background_image = pg.image.load(IMAGES + '\menu\\font3.png')
        surface_image = pg.image.load(IMAGES + '\menu\Menu2.png')
        surface_image = pg.transform.scale(surface_image, (int(
            surface_image.get_width()*0.8), int(surface_image.get_height()*0.8)))
        label_image = pg.image.load(IMAGES + '\menu\Menu.png')
        # label_image = pg.transform.scale(label_image, (int(label_image.get_width()*0.8), int(label_image.get_height()*0.8)))
        exit_image = pg.image.load(IMAGES + '\menu\Quite.png')
        continue_image = pg.image.load(IMAGES + '\menu\Continue.png')
        restart_image = pg.image.load(IMAGES + '\menu\Restart.png')
        settings_image = pg.image.load(IMAGES + '\menu\Settings.png')

        self.blured_background = ImageSurface((0,0), blured_background_image, center=False)
        self.surface = ImageSurface(
            [self.width/2, self.height/2], surface_image.convert_alpha(), center=True)
        self.label = ImageSurface(
            [self.surface.rect.centerx, self.surface.rect.top+label_image.get_height()*1.5], label_image.convert_alpha(), center=True)
        self._continue = ImageButton([self.surface.rect.centerx, self.surface.rect.top+exit_image.get_height(
        )*4.5], continue_image.convert_alpha(), center=True, func=self.aplication.showMenu)
        self.settings = ImageButton([self.surface.rect.centerx, self.surface.rect.top +
                                    exit_image.get_height()*6.5], settings_image.convert_alpha(), center=True, func=None)
        self.restart = ImageButton([self.surface.rect.centerx, self.surface.rect.top +
                                   exit_image.get_height()*8.5], restart_image.convert_alpha(), center=True, func=self.aplication.restart)
        self.exit = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+exit_image.get_height()*10.5], exit_image.convert_alpha(), center=True, func=self.aplication.close)

        self.btnGroup = CustomGroup(
            self.surface, self.label, self.exit, self._continue, self.restart, self.settings)

    def draw(self, display):
        self.btnGroup.draw(display)
        self.blured_background.draw(display)

    def execute(self):
        for btn in self.btnGroup:
            if btn.rect.collidepoint(pg.mouse.get_pos()):
                btn.execute()

    def update(self):
        for sprite in self.btnGroup:
            if sprite.rect.collidepoint(pg.mouse.get_pos()):
                sprite.isHover = True
            else:
                sprite.isHover = False
