import logging
import pygame as pg
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle
import sys
import ctypes
from levels import Level
from GUI.menu import EnterMenu, Menu, DieMenu, WinMenu, SettingsMenu
from GUI.elements import Text
from interface import Toolbar
from changed_group import Groups, spritecollide
from settings import IMAGES
from timer import Timer


class BaseStrategy:
    def __init__(self, mediator):
        self.aplication = mediator

    def draw(self, display, *args, **kwargs):
        pass

    def update(self):
        # self.aplication.controller.update()
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
        _now = Timer.get_ticks()
        self.aplication.controller.changePlayerDirection(
            self.aplication.player)
        self.aplication.controller.update()
        self.aplication.toolbar.update()
        self.aplication.groups.update(
            now=_now,
            display_size=self.aplication.display_size,
            player_center=self.aplication.player.rect.center,
            joystick_hover_point=self.aplication.controller.hoverPointPos if hasattr(
                self.aplication.controller, 'hoverPointPos') else None
        )
        self.aplication.groups.collide(self.aplication.player)
        self.aplication.player.update(now=_now)

        if self.aplication.player.HP <= 0:
            self.aplication.showDieMenu(True)
            return

        self.aplication.level.update(now=_now)

        if self.aplication.level.isWin:
            self.aplication.setWinMenuStrategy()

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
        self.aplication.controller.selectUltimate(
            self.aplication.player, event)
        self.aplication.controller.showMenu(event)

        if event.type == self.aplication.game_timer.timer_update_event:
            self.aplication.game_timer.update()

        return super().eventListen(event)


class BaseMenuStrategy(BaseStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = Menu(self.aplication, self.aplication.display_size)

    def update(self):
        self.aplication.controller.update()
        return super().update()

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


class WinMenuStrategy(BaseMenuStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = WinMenu(mediator, mediator.display_size)


class EnterMenuStrategy(BaseMenuStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = EnterMenu(mediator, mediator.display_size)


class SettingsMenuStrategy(BaseMenuStrategy):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = SettingsMenu(mediator, mediator.display_size)

    def eventListen(self, event):
        super().eventListen(event)
        self.aplication.controller.back(event)
        return


class Aplication:
    controller = None
    controleRealization = {
        KeyboardControle.name: KeyboardControle,
        JoystickControle.name: JoystickControle
    }
    controleRealizationIndex = 0
    menuStrategy: BaseStrategy = MenuStrategy
    gameStrategy: BaseStrategy = GameStrategy
    dieMenuStrategy: BaseStrategy = DieMenuStrategy
    winMenuStrategy: BaseStrategy = WinMenuStrategy
    guiMenuStrategy: BaseStrategy = EnterMenuStrategy
    settingsMenuStrategy: BaseStrategy = SettingsMenuStrategy

    inventoryStrategy: BaseStrategy = None
    _actingStrategy = None
    isMenu = False
    isPlayerDie = False
    isInterface = False
    isSettings = False
    isFPS = True
    _lastStrategy = None

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

        self._acting_level: Level = level

        self.menuStrategy = self.menuStrategy(self)
        self.dieMenuStrategy = self.dieMenuStrategy(self)
        self.gameStrategy = self.gameStrategy(self)
        self.guiMenuStrategy = self.guiMenuStrategy(self)
        self.winMenuStrategy = self.winMenuStrategy(self)
        self.settingsMenuStrategy = self.settingsMenuStrategy(self)
        self._actingStrategy = self.guiMenuStrategy
        self._lastStrategy = self._actingStrategy

    def start(self):
        """main aplicatiodn start function"""
        log.info('start app')
        fontFPS = Text([self.display_size[0]*0.9, 20], str(int(self.clock.get_fps())),
                       40, (0, 255, 26), False, 'hooge0554')
        image = pg.image.load(
            IMAGES + "\\game_objects\\strike_point.png").convert_alpha()
        rect = image.get_rect(center=(0, 0))

        while self.__run:
            for event in pg.event.get():
                self._actingStrategy.eventListen(event)

            self._actingStrategy.draw(self.display)
            self._actingStrategy.update()

            if self.isFPS:
                fontFPS.draw(self.display)
                fontFPS.update(text=str(int(self.clock.get_fps())))

            # self.display.blit(image, rect)
            # rect.center = pg.mouse.get_pos()

            pg.display.update()
            dt = self.clock.tick(60)

    def changeControllerToggle(self):
        self.controleRealizationIndex += 1
        if self.controleRealizationIndex >= len(self.controleRealization.values()):
            self.controleRealizationIndex = 0

        self._setControllerType(list(self.controleRealization.keys())[
                                self.controleRealizationIndex])

    def _setControllerType(self, controllerType: str, *args, **kwargs):
        """set controller type by name (controllerType)"""
        if controllerType in self.controleRealization:
            if not self.controller:
                self.controller = self.controleRealization[controllerType](
                    ControlImplementation(self, *args, **kwargs))

            else:
                _controleImpl = self.controller.getImpl()
                self.controller = self.controleRealization[controllerType](
                    _controleImpl)

        log.info(f'Controller was removed to {self.controller.type()}')

    def getControllerType(self):
        return str(self.controller.name)

    def setWinMenuStrategy(self, value: bool = None):
        self._actingStrategy = self.winMenuStrategy
        log.info(
            f"level <{self._acting_level.__class__.__name__}> was completed")

    def showMenu(self, value: bool = None):
        log.debug('show menu')
        """Show and close menu"""
        if value != None:
            self.isMenu = value
        else:
            self.isMenu = not self.isMenu

        if self.isMenu:
            self._actingStrategy = self.menuStrategy
        else:
            self._actingStrategy = self.gameStrategy

    def showFPS(self, value: bool = None):
        if value != None:
            self.isFPS = value
        else:
            self.isFPS = not self.isFPS

    def showDieMenu(self, value: bool = None):
        log.debug('show die menu')
        if value != None:
            self.isPlayerDie = value
        else:
            self.isPlayerDie = not self.isPlayerDie

        if self.isPlayerDie:
            self._actingStrategy = self.dieMenuStrategy
        else:
            self._actingStrategy = self.gameStrategy

    def showSettings(self, value: bool = None):
        log.debug('show settings')
        if self._actingStrategy == self.settingsMenuStrategy:
            self.isSettings = True
        else:
            self.isSettings = False

        if value != None:
            self.isSettings = value
        else:
            self.isSettings = not self.isSettings

        if self.isSettings:
            self._lastStrategy = self._actingStrategy
            self._actingStrategy = self.settingsMenuStrategy
        else:
            self._actingStrategy = self._lastStrategy

    def backToLastStrategy(self):
        self._actingStrategy = self._lastStrategy

    def startGame(self, *args, **kwargs):
        log.info('start level')
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

    def close(self):
        log.info('close app')
        self.quitGame()
        self.__run = False

    def leaveToMenu(self):
        self._actingStrategy = self.guiMenuStrategy
        self.quitGame()

    def changeLevel(self, level: Level):
        self.level = level(self, self.groups)
        self.groups.Background.empty()
        self.level.start()

    def restart(self):
        log.info("restart level")
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
    import logger
    # file_name='app_info.log' -> will write logs into file
    log = logger.setup_logger()
    aplication = Aplication(Level1)
    # aplication.changeLevel(AsteroidWaves)
    aplication.start()
