from typing_extensions import runtime

from pygame import display
from lavels import Level, Level1
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle, BaseController
# from display import Display
import pygame as pg
from pygame.sprite import Group
import sys
from pygame import Surface
import ctypes
from menu import ColoredSurface


class Groups:
    def __init__(self):
        self.enemyGroup = Group()
        self.playerShell = Group()
        self.objectsGroup = Group()
        self._groups = [self.enemyGroup, self.playerShell, self.objectsGroup]

    def collideAll(self):
        pass

    def update(self, *args, **kwargs):
        for _group in self._groups:
            _group.update(*args, **kwargs)

    def draw(self, display, *args, **kwargs):
        for _group in self._groups:
            _group.draw(display)

    def count(self):
        _counter = 0
        for _group in self._groups:
            _counter += len(_group.sprites())
        return _counter


class BaseStrategy:
    name = None

    def __init__(self, mediator):
        self.aplication = mediator

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


class GameStrategy(BaseStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)

    def update(self):
        _now = pg.time.get_ticks()
        self.aplication.controller.changePlayerDirection(
            self.aplication.player)

        self.aplication.display.fill((10, 9, 15))

        self.aplication.groups.update(
            now=_now, display_size=self.aplication.display_size)
        self.aplication.groups.draw(self.aplication.display)

        self.aplication.player.update(now=_now)
        self.aplication.player.draw(self.aplication.display)

        self.aplication.level.update(now=_now)
        # print(self.aplication.groups.enemyGroup)

        return super().update()

    def eventListen(self, event):
        self.aplication.controller.executeWeapon(
            self.aplication.player, event)
        self.aplication.controller.changeWeapon(
            self.aplication.player, event)

        return super().eventListen(event)


class MenuStrategy(BaseStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        width = self.aplication.display.get_width() / 1.5
        height = self.aplication.display.get_height() / 1.5
        self.bigBtn = ColoredSurface(
            pos=self.aplication.display.get_rect().center,
            size=(width, height),
            center=True,
            color=(100, 150, 230),
            border_radius=15)

    def update(self):
        self.bigBtn.draw(self.aplication.display)
        return super().update()

    def eventListen(self, event):
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
        user32 = ctypes.windll.user32

        self.window_size = user32.GetSystemMetrics(
            0), user32.GetSystemMetrics(1)
        self.display_size = (
            int(0.4*self.window_size[0]), int(0.9*self.window_size[1]))
        self.display = pg.display.set_mode(self.display_size)

        self.clock = pg.time.Clock()
        self.groups = Groups()

        self.player = Player(self.display_size, self, self.groups.playerShell)
        self.controller = self.controleRealization[controllerType](
            ControlImplementation(self, *args, **kwargs))

        self.menuStrategy = self.menuStrategy(self)
        self.gameStrategy = self.gameStrategy(self)
        self._actingStrategy = self.gameStrategy
        self.level = level(self, enemyGroup=self.groups.enemyGroup)
        self.level.start()

    def setController(self, controllerType: str, *args, **kwargs):
        """set controller type by name (controllerType)"""
        if controllerType in self.controleRealization:
            if not self.controller:
                self.controller = self.controleRealization[controllerType](
                    ControlImplementation(self, *args, **kwargs))

            else:
                _controleImpl = self.controller.getImpl()
                self.controller = self.controleRealization[controllerType](
                    _controleImpl)

        return f'Controller was removed to {self.controller.type()}'

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
            pg.display.update()
            self.clock.tick(60)

    def close(self):
        self.__run = False


if __name__ == '__main__':
    aplication = Aplication(Level1)
    # aplication.setController('joystick')
    aplication.start()


"""
1. Нужно использовать паттерн комманда, чтобы вызывать меню игры и 1
выполянять другие действия. 
2. Использовать паттерн Bridge, чтобы сделать управление через несколько
вариаций устройств
2.2 Вынести максимально возможное количество функций программы в абстрактные 
классы и функции
2.3 Конкретизировать классы только способом взаимодействия с этими функциями
"""
