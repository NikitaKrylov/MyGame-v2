import pygame as pg
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle
import sys
import ctypes
from lavels import Level
from menu import Menu
from interface import Toolbar
from changed_group import Groups, spritecollide
from settings import IMAGES
"""RenderUpdates - в методе draw возвращdaает изменения rect"""


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

    def __str__(self):
        return self.__class__.__name__


class InventoryStrategy(BaseStrategy):
    def draw(self, display, *args, **kwargs):
        pass

    def update(self):
        pass

    def eventListen(self, event):
        return super().eventListen(event)


class GameStrategy(BaseStrategy):
    def update(self, *args, **kwargs):
        _now = pg.time.get_ticks()
        self.aplication.controller.changePlayerDirection(
            self.aplication.player)
        self.aplication.toolbar.update()
        self.aplication.groups.update(
            now=_now,
            display_size=self.aplication.display_size,
            player_center=self.aplication.player.rect.center)
        self.aplication.groups.collide(self.aplication.player)
        self.aplication.player.update(now=_now)
        self.aplication.level.update(now=_now)

        if self.aplication.player.HP <= 0:
            self.aplication.close()
            print('You lose')

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
        return super().update()

    def draw(self, display):
        self.menu.draw(display)

    def eventListen(self, event):
        self.aplication.controller.menuUpdate(event)
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
        self.display_size = [int(0.4*self.window_size[0]),
                             int(0.9*self.window_size[1])]
        print(self.display_size)
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
        self.level = level(self, self.groups)
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
            self.isMenu = True
        else:
            self._actingStrategy = self.gameStrategy
            self.isMenu = False

    def start(self):
        """main aplicatiodn start function"""
        while self.__run:
            for event in pg.event.get():
                self._actingStrategy.eventListen(event)

            self._actingStrategy.update()
            self._actingStrategy.draw(self.display)
            pg.display.update()
            self.clock.tick(60)

    def close(self):
        self.__run = False

    def changeLevel(self, level: Level):
        print(f"""
              Level was removed to { self.level}
              """)
        self.level = level(self, self.groups)
        self.groups.Background.empty()
        self.level.start()
        return

    def restart(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.groups.restart()
        self.level.restart()
        self.level.start()
        self.player.restart()
        self.toolbar = Toolbar(self.display_size, self.player.equipment)

        self.showMenu()


if __name__ == '__main__':
    from lavels import AsteroidWaves, Level1
    aplication = Aplication(Level1)
    # aplication.changeLevel(AsteroidWaves)
    # aplication.setControllerType('joystick')
    aplication.start()
