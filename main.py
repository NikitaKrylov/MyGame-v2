import pygame as pg
from pygame import display
from pygame import image
from pygame import event
from pygame import draw
from lavels import Level, Level1
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle, BaseController
from pygame.sprite import Group, RenderUpdates
import sys
from pygame import Surface
import ctypes
from menu import Menu, Text
from interface import Toolbar
from sprite import Groups, spritecollide
"""RenderUpdates - в методе draw возвращает изменения rect"""


class BaseStrategy:
    def __init__(self, mediator):
        self.aplication = mediator

    def draw(self, display, *args, **kwargs):
        pass

    def update(self):
        """default update aplication function"""

    def eventListen(self, event):
        """update aplication function with event attributs"""
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        self.aplication.controller.showMenu(event)

    @property
    def type(self):
        return self.__class__.__name__


class InventoryStrategy(BaseStrategy):
    def draw(self, display, *args, **kwargs):
        pass

    def update(self):
        pass

    def eventListen(self, event):
        return super().eventListen(event)


class GameStrategy(BaseStrategy):
    def update(self):
        _now = pg.time.get_ticks()
        self.aplication.controller.changePlayerDirection(
            self.aplication.player)
        self.aplication.toolbar.update()
        self.aplication.groups.update(
            now=_now, display_size=self.aplication.display_size)
        self.aplication.groups.collide(self.aplication.player)
        self.aplication.player.update(now=_now)
        self.aplication.level.update(now=_now)

        return super().update()

    def draw(self, display):
        display.fill((10, 9, 15))
        self.aplication.groups.draw(display)
        self.aplication.player.draw(display)
        self.aplication.toolbar.draw(display)

    def eventListen(self, event):
        self.aplication.controller.executeWeapon(
            self.aplication.player, event)
        self.aplication.controller.changeWeapon(
            self.aplication.player, event)

        return super().eventListen(event)


class MenuStrategy(BaseStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = Menu(self.aplication, self.aplication.display_size)

    def update(self):
        self.menu.update()
        return super().update()

    def draw(self, display):
        self.menu.draw(display)

    def eventListen(self, event):
        self.aplication.controller.menuExecute(event)
        return super().eventListen(event)


class Aplication:
    controller = None
    controleRealization = {
        KeyboardControle.name: KeyboardControle,
        JoystickControle.name: JoystickControle
    }
    menuStrategy: BaseStrategy = MenuStrategy
    gameStrategy: BaseStrategy = GameStrategy
    inventoryStrategy: BaseStrategy = None
    _actingStrategy = None
    isMenu = False
    isInterface = False
    __run = True
    ticks = 0

    def __init__(self, level: Level, controllerType: str = 'keyboard', *args, **kwargs):
        pg.init()
        pg.font.init()
        user32 = ctypes.windll.user32

        self.window_size = user32.GetSystemMetrics(
            0), user32.GetSystemMetrics(1)
        self.display_size = (
            int(0.4*self.window_size[0]), int(0.9*self.window_size[1]))
        self.display = pg.display.set_mode(self.display_size)

        self.clock = pg.time.Clock()
        self.groups = Groups()

        self.player = Player(self.display_size, self,
                             self.groups.playerShell, self.groups.Particles)
        self.controller = self.controleRealization[controllerType](
            ControlImplementation(self, *args, **kwargs))

        self.toolbar = Toolbar(self.display_size, self.player.equipment)

        self.menuStrategy = self.menuStrategy(self)
        self.gameStrategy = self.gameStrategy(self)
        self._actingStrategy = self.gameStrategy
        self.level = level(self, enemyGroup=self.groups.enemyGroup)
        self.level.start()

    def setControllerType(self, controllerType: str, *args, **kwargs):
        """set controller type by name (controllerType)"""
        if controllerType in self.controleRealization:
            if not self.controller:
                self.controller = self.controleRealization[controllerType](
                    ControlImplementation(self, *args, **kwargs))

            else:
                _controleImpl = self.controller.getImpl()
                self.controller = self.controleRealization[controllerType](
                    _controleImpl)

        return print(f'Controller was removed to {self.controller.type()}')

    def showMenu(self):
        """Show and close menu"""
        if not self.isMenu:
            self._actingStrategy = self.menuStrategy
            self.isMenu = not self.isMenu
        else:
            self._actingStrategy = self.gameStrategy
            self.isMenu = not self.isMenu

    def start(self):
        """main aplication start function"""
        while self.__run:
            for event in pg.event.get():
                self._actingStrategy.eventListen(event)

            self._actingStrategy.update()
            self._actingStrategy.draw(self.display)
            pg.display.update()
            self.clock.tick(60)

    def close(self):
        self.__run = False

    def restart(self):
        pg.init()
        self.groups.restart()
        self.level.restart()
        self.level.start()
        self.player.restart()
        
        self.showMenu()

if __name__ == '__main__':
    aplication = Aplication(Level1)
    # aplication.setControllerType('joystick')
    aplication.start()
