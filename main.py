import pygame as pg
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle
import sys
import ctypes
from levels import Level
from menu import Menu, DieMenu, AplicationMenu, Text
from interface import Toolbar
from changed_group import Groups, spritecollide
from settings import IMAGES
"""RenderUpdates - в методе draw возвращdaает изменения rect"""


class Timer:
    def __init__(self):
        self.ticks = 0
        self.timer_update_event = pg.USEREVENT+1
        pg.time.set_timer(self.timer_update_event, 1)

    def update(self):
        self.ticks += 1

    def reset(self):
        self.ticks = 0

    def get_ticks(self):
        return self.ticks

    def __str__(self):
        return str(self.ticks)


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
        # _now = pg.time.get_ticks()
        _now = self.aplication.game_timer.get_ticks()
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
            self.aplication.showDieMenu()
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
        self.aplication.controller.showMenu(event)

        if event.type == self.aplication.game_timer.timer_update_event:
            self.aplication.game_timer.update()

        return super().eventListen(event)


class BaseMenuStrategy(BaseStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = Menu(self.aplication, self.aplication.display_size)

    def draw(self, display):
        self.menu.draw(display)

    def eventListen(self, event):
        self.aplication.controller.menuUpdate(event)
        self.aplication.controller.menuExecute(event)
        return super().eventListen(event)


class MenuStrategy(BaseMenuStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = Menu(self.aplication, self.aplication.display_size)

    def eventListen(self, event):
        super().eventListen(event)
        self.aplication.controller.showMenu(event)
        return


class DieMenuStrategy(BaseMenuStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = DieMenu(mediator, mediator.display_size)


class GUIMenuStrategy(BaseMenuStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = AplicationMenu(mediator, mediator.display_size)


class Aplication:
    controller = None
    controleRealization = {
        KeyboardControle.name: KeyboardControle,
        JoystickControle.name: JoystickControle
    }
    menuStrategy: BaseStrategy = MenuStrategy
    gameStrategy: BaseStrategy = GameStrategy
    dieMenuStrategy: BaseStrategy = DieMenuStrategy
    guiMenuStrategy: BaseStrategy = GUIMenuStrategy
    inventoryStrategy: BaseStrategy = None
    _actingStrategy = None
    isMenu = False
    isPlayerDie = False
    isInterface = False
    __run = True
    ticks = 0

    def __init__(self, level: Level, controllerType: str = 'keyboard', *args, **kwargs):
        pg.init()
        pg.font.init()
        user32 = ctypes.windll.user32
        self.clock = pg.time.Clock()

        self.game_timer = Timer()
        self.window_size = user32.GetSystemMetrics(
            0), user32.GetSystemMetrics(1)
        self.display_size = [int(0.4*self.window_size[0]),
                             int(0.9*self.window_size[1])]
        self.display = pg.display.set_mode(self.display_size)
        self.controller = self.controleRealization[controllerType](
            ControlImplementation(self, *args, **kwargs))

        self._acting_level = level

        # self.clock = pg.time.Clock()
        # self.groups = Groups()

        # self.player = Player(self.display_size, self,
        #                      self.groups.playerShell, self.groups.Particles)

        self.menuStrategy = self.menuStrategy(self)
        self.dieMenuStrategy = self.dieMenuStrategy(self)
        self.gameStrategy = self.gameStrategy(self)
        self.guiMenuStrategy = self.guiMenuStrategy(self)
        # self._actingStrategy = self.gameStrategy

        # self.startGame(level)
        self._actingStrategy = self.guiMenuStrategy
        # self.level.start()

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

    def showMenu(self, value: bool = None):
        """Show and close menu"""
        if value != None:
            self.isMenu = value
        else:
            self.isMenu = not self.isMenu

        if self.isMenu:
            self._actingStrategy = self.menuStrategy
        else:
            self._actingStrategy = self.gameStrategy

    def showDieMenu(self):
        if not self.isPlayerDie:
            self._actingStrategy = self.dieMenuStrategy
            self.isPlayerDie = True
        else:
            self._actingStrategy = self.gameStrategy
            self.isPlayerDie = False

    def startGame(self, *args, **kwargs):
        self.groups = Groups()

        self.player = Player(self.display_size, self,
                             self.groups.playerShell, self.groups.Particles)
        self.toolbar = Toolbar(self.display_size, self.player.equipment)
        self.level = self._acting_level(self, self.groups)
        self.level.start()

        self._actingStrategy = self.gameStrategy

    def quitGame(self):
        self.level = None
        self.player = None
        self.game_timer.reset()
        self.toolbar = None
        self.groups = None
        self.isMenu = False
        self.isPlayerDie = False

        self._actingStrategy = self.guiMenuStrategy

    def start(self):
        """main aplicatiodn start function"""
        fontFPS = Text([self.display_size[0]*0.9, 20], str(int(self.clock.get_fps())),
                       40, (0, 255, 26), False, 'hooge0554')

        while self.__run:
            for event in pg.event.get():
                self._actingStrategy.eventListen(event)

            self._actingStrategy.update()
            self._actingStrategy.draw(self.display)
            fontFPS.draw(self.display)
            fontFPS.update(text=str(int(self.clock.get_fps())))
            pg.display.update()
            dt = self.clock.tick(60)
            # print(self.clock.get_fps())

    def close(self):
        self.quitGame()
        self.__run = False

    def leaveToMenu(self):
        self._actingStrategy = self.guiMenuStrategy
        self.quitGame()

    def changeLevel(self, level: Level):
        print(f"""
              Level was removed to { self.level}
              """)
        self.level = level(self, self.groups)
        self.groups.Background.empty()
        self.level.start()

    def restart(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.groups.restart()
        self.level.restart()
        self.level.start()
        self.player.restart()
        self.toolbar = Toolbar(self.display_size, self.player.equipment)
        self.game_timer.reset()
        self.showMenu(value=False)


if __name__ == '__main__':
    from levels import AsteroidWaves, Level1
    aplication = Aplication(Level1)
    # aplication.changeLevel(AsteroidWaves)
    # aplication.setControllerType('joystick')
    aplication.start()
