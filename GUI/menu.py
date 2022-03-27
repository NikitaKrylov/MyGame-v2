import random
from typing import Tuple
import pygame as pg
from pygame.font import Font
from settings import IMAGES, MEDIA
from changed_group import CustomGroup
from .surface import ImageSurface, ColoredSurface, Text, BaseSurface
from .button import ImageButton, TextToggleButton

# This class is the base class for all menus. It contains all the basic functions that all menus share


class BaseMenu:
    def __init__(self, mediator, display_size):
        self.aplication = mediator
        self.display_size = (self.width, self.height) = display_size
        self.backgroundPiecesGroup = CustomGroup()
        self.btnGroup = CustomGroup()

    def draw(self, display, *args, **kwargs):
        self.backgroundPiecesGroup.draw(display)
        self.btnGroup.draw(display)

    def update(self, *args, **kwargs):
        self.backgroundPiecesGroup.update(*args, **kwargs)
        self.btnGroup.update(*args, **kwargs)

        if kwargs.get("isController"):
            key = kwargs.get("controller")
            i = key % self.btnGroup.__len__()

            for j in range(self.btnGroup.__len__()):
                if j == i:
                    self.btnGroup.sprites()[j].isHover = True
                else:
                    self.btnGroup.sprites()[j].isHover = False
        else:

            for sprite in self.btnGroup:
                if sprite.rect.collidepoint(pg.mouse.get_pos()):
                    sprite.isHover = True
                else:
                    sprite.isHover = False

    def execute(self, *args, **kwargs):
        if kwargs.get("isController"):
            key = kwargs.get("controller")
            i = key % self.btnGroup.__len__()
            self.btnGroup.sprites()[i].execute()
            return

        else:
            for btn in self.btnGroup:
                if btn.rect.collidepoint(pg.mouse.get_pos()):
                    btn.execute()

    @staticmethod
    def ImageScale(surface: pg.Surface, scale_index: float):
        width, height = surface.get_size()
        return pg.transform.scale(surface, int(width*scale_index), int(height*scale_index))


"""---------------------------GAME MENU--------------------------------"""


class GameMenu(BaseMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)
        self.background = ColoredSurface(
            (0, 0), self.display_size, center=False, color=pg.Color(21, 37, 46, 35))

        self.backgroundPiecesGroup.add(self.background)


class Menu(GameMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)
        surface_image = pg.image.load(IMAGES + '\\menu\\Menu2.png')
        surface_image = pg.transform.scale(surface_image, (int(
            surface_image.get_width()*0.8), int(surface_image.get_height()*0.8)))
        label_image = pg.image.load(IMAGES + '\\menu\\Menu.png')
        continue_image = pg.image.load(IMAGES + '\\menu\\Continue.png')
        restart_image = pg.image.load(IMAGES + '\\menu\\Restart.png')
        leave_image = pg.image.load(IMAGES + '\\menu\\Leave.png')
        settings_image = pg.image.load(IMAGES + '\\menu\\Settings.png')

        self.surface = ImageSurface(
            [self.width/2, self.height/2], surface_image.convert_alpha(), center=True)
        self.label = ImageSurface(
            [self.surface.rect.centerx, self.surface.rect.top+label_image.get_height()*1.5], label_image.convert_alpha(), center=True)
        self._continue = ImageButton([self.surface.rect.centerx, self.surface.rect.top+continue_image.get_height(
        )*4.5], continue_image.convert_alpha(), center=True, func=self.aplication.showMenu)
        self.settings = ImageButton([self.surface.rect.centerx, self.surface.rect.top +
                                    continue_image.get_height()*6.4], settings_image.convert_alpha(), center=True, func=self.aplication.showSettings)
        self.restart = ImageButton([self.surface.rect.centerx, self.surface.rect.top +
                                   continue_image.get_height()*8.1], restart_image.convert_alpha(), center=True, func=self.aplication.restart)
        self.leave = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+continue_image.get_height()*10], leave_image.convert_alpha(), center=True, func=self.aplication.leaveToMenu)

        self.backgroundPiecesGroup.add(self.surface, self.label)
        self.btnGroup.add(self._continue, self.settings,
                          self.restart, self.leave)


class FinaleMenu(BaseMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)
        surface_image = pg.image.load(IMAGES + '\menu\Menu2.png')
        surface_image = pg.transform.scale(surface_image, (int(
            surface_image.get_width()*0.8), int(surface_image.get_height()*0.8)))
        exit_image = pg.image.load(IMAGES + '\menu\Quite.png')
        restart_image = pg.image.load(IMAGES + '\menu\Restart.png')
        leave_image = pg.image.load(IMAGES + '\menu\Leave.png')

        self.surface = ImageSurface(
            [self.width/2, self.height/2], surface_image.convert_alpha(), center=True)
        self.restart = ImageButton([self.surface.rect.centerx, self.surface.rect.top +
                                   exit_image.get_height()*5.5], restart_image.convert_alpha(), center=True, func=self.aplication.restart)
        self.leave = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+leave_image.get_height()*6.45], leave_image.convert_alpha(), center=True, func=self.aplication.leaveToMenu)
        self.exit = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+exit_image.get_height()*8.5], exit_image.convert_alpha(), center=True, func=self.aplication.close)

        self.backgroundPiecesGroup.add(self.surface)
        self.btnGroup.add(self.restart,  self.leave)


class DieMenu(FinaleMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)

        label_image = pg.image.load(IMAGES + '\menu\YouDied.png')
        self.label = ImageSurface(
            [self.surface.rect.centerx, self.surface.rect.top+label_image.get_height()*1.5], label_image.convert_alpha(), center=True)

        self.backgroundPiecesGroup.add(self.label)
        self.btnGroup.add(self.restart)


class WinMenu(FinaleMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)

        label_image = pg.image.load(IMAGES + '\\menu\\YouWon.png')
        next_image = pg.image.load(IMAGES + '\\menu\\Next.png')
        self.label = ImageSurface(
            [self.surface.rect.centerx, self.surface.rect.top+label_image.get_height()*1.5], label_image.convert_alpha(), center=True)
        self.next = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+next_image.get_height()*8], next_image.convert_alpha(), center=True, func=None)

        self.backgroundPiecesGroup.add(self.label)
        self.btnGroup.add(self.restart, self.next)


class InventoryMenu(GameMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)

        surface = pg.image.load(IMAGES + '\\menu\\backgroundMenu.png')
        self.surface = ImageSurface(
            (self.width//2, self.height//2), surface, center=True)
        self.label = Text((self.width//2, int(self.surface.rect.top+self.surface.rect.height*0.2)),
                          "Inventory", (255, 255, 255), Font(MEDIA + '\\font\\karmasuture.ttf', 36), True)

        self.backgroundPiecesGroup.add(self.surface, self.label)


"""---------------------------APLICATION MENU--------------------------------"""


class AbstractAplicationMenu(BaseMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)
        self.surface = ColoredSurface(
            (0, 0), self.display_size, False, (24, 38, 41))
        self.backgroundPiecesGroup.add(self.surface)

        for _ in range(random.randint(13, 23)):
            width = random.randint(
                int(self.display_size[0]*0.01), int(self.display_size[0]*0.15))
            ColoredSurface(
                (random.randint(1, self.display_size[0]), random.randint(
                    1, self.display_size[1])),
                (width, width),
                center=True,
                color=(17, 31,  34)
            ).add(self.backgroundPiecesGroup)


class EnterMenu(AbstractAplicationMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)
        start_image = pg.image.load(IMAGES + '\\menu\\Start.png')
        change_level_image = pg.image.load(IMAGES + '\\menu\\ChangeLevel.png')
        exit_image = pg.image.load(IMAGES + '\\menu\\Quite.png')
        settings_image = pg.image.load(IMAGES + '\\menu\\Settings.png')

        self.start = ImageButton([self.surface.rect.centerx, self.surface.rect.top +
                                 exit_image.get_height()*3], start_image, center=True, func=self.aplication.startGame)
        self.change_level = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+exit_image.get_height()*5.5], change_level_image, center=True, func=self.aplication.showLevelManager)
        self.settings = ImageButton([self.surface.rect.centerx, self.surface.rect.top+exit_image.get_height(
        )*8], settings_image, center=True, func=self.aplication.showSettings)
        self.exit = ImageButton(
            [self.surface.rect.centerx, self.surface.rect.top+exit_image.get_height()*10.5], exit_image.convert_alpha(), center=True, func=self.aplication.close)

        self.btnGroup.add(self.start, self.change_level,
                          self.settings, self.exit)


class SettingsMenu(AbstractAplicationMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)
        font = pg.font.Font(
            MEDIA + '\\font\\karmasuture.ttf', 36)

        toggle_controller_type_image1 = font.render(
            self.aplication.getControllerType(), False, (255, 255, 255))
        toggle_controller_type_image2 = font.render(
            "Find...", False, (255, 255, 255))
        toggle_FPS_image1 = font.render("show FPS", False, (255, 255, 255))
        toggle_FPS_image2 = font.render(
            "don`t show FPS", False, (255, 255, 255))

        self.toggle_controller_type = TextToggleButton(
            [self.surface.rect.centerx, self.surface.rect.centery], toggle_controller_type_image1, onClickImage=toggle_controller_type_image2, func=self.aplication.changeControllerToggle, font=font, center=True)
        self.toggle_FPS = TextToggleButton(
            [self.surface.rect.centerx, self.surface.rect.centery+toggle_controller_type_image1.get_height()*2], toggle_FPS_image1, onClickImage=toggle_FPS_image2, func=self.aplication.showFPS, font=font, center=True)

        # Grid(self.display_size, 120, 100, self.toggle_controller_type, self.toggle_FPS).Set()

        self.btnGroup.add(self.toggle_controller_type, self.toggle_FPS)

    def update(self, *args, **kwargs):
        self.toggle_controller_type.changeImage(
            text=self.aplication.getControllerType())
        return super().update(*args, **kwargs)


class LevelManagerMenu(AbstractAplicationMenu):
    def __init__(self, mediator, display_size):
        super().__init__(mediator, display_size)


"""---------------------------GRIDS--------------------------------"""


class Grid:
    margin = 0
    padding = 0

    def __init__(self, display_size: list, margin=0, padding=0, *objects: Tuple[BaseSurface]):
        self.display_size = display_size
        self.margin = margin
        self.padding = padding
        self.objects = objects

    def Set(self):
        xpos = self.margin
        for obj in self.objects:
            if xpos + obj.rect.width + self.padding < self.display_size[0] - self.margin:
                obj.rect.left = xpos + self.margin
                xpos = obj.rect.right


class CenterGrid(Grid):
    margin = 0
    padding = 0
