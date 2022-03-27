import pygame as pg
from pygame.font import SysFont
from GameObjects.ultimates import Striker
from gui.interface import EquipmentDrawer
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle
import sys
import ctypes
from level.levelManager import LevelManager
from gui.menu import EnterMenu, Menu, DieMenu, WinMenu, SettingsMenu, InventoryMenu, LevelManagerMenu
from gui.surface import Text
from changed_group import Groups
from timer import Timer

"""----------------------------BASE MENU------------------------------------"""

# The base strategy class is the base class for all the other strategy classes.
# It contains the basic functions that are needed to run the aplication.


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
            log.info('close app')
            pg.quit()
            sys.exit()

    @property
    def type(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__


"""----------------------------GAME------------------------------------"""


class GameStrategy(BaseStrategy):
    def update(self, *args, **kwargs):
        self.aplication.controller.changePlayerDirection(
            self.aplication.player)
        self.aplication.controller.update()
        self.aplication.groups.collide(self.aplication.player)
        self.aplication.player.update()

        if self.aplication.player.HP <= 0:
            self.aplication.showDieMenu(True)
            return

        self.aplication.levelManager.Update()

        if self.aplication.levelManager.GetActingLevel().isWin:
            self.aplication.setWinMenuStrategy()

        return super().update()

    def draw(self, display):
        display.fill((10, 9, 15))
        self.aplication.groups.draw(display)
        self.aplication.player.draw(display)
        # self.aplication.toolbar.draw(display)

    def eventListen(self, event):
        self.aplication.controller.executeWeapon(
            self.aplication.player, event)
        self.aplication.controller.changeWeapon(
            self.aplication.player, event)
        self.aplication.controller.changeUltimate(
            self.aplication.player, event)
        self.aplication.controller.selectUltimate(
            self.aplication.player, event)
        self.aplication.controller.showInventory(event)
        self.aplication.controller.showMenu(event)

        if event.type == self.aplication.game_timer.timer_update_event:
            self.aplication.game_timer.update()

        if event.type == self.aplication.game_timer.sprite_group_update_event:
            self.aplication.groups.update(
                display_size=self.aplication.display_size,
                player_center=self.aplication.player.rect.center,
                joystick_hover_point=self.aplication.controller.hoverPointPos if hasattr(
                    self.aplication.controller, 'hoverPointPos') else None
            )

        return super().eventListen(event)


"""----------------------------GAME MENU------------------------------------"""


class BaseMenuStrategy(BaseStrategy):
    menu_class = Menu

    def __init__(self, mediator):
        super().__init__(mediator)

        self.menu = self.__class__.menu_class(
            self.aplication, self.aplication.display_size)

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
    menu_class = Menu

    def eventListen(self, event):
        super().eventListen(event)
        self.aplication.controller.showMenu(event)
        return


class DieMenuStrategy(BaseMenuStrategy):
    menu_class = DieMenu


class WinMenuStrategy(BaseMenuStrategy):
    menu_class = WinMenu


"""----------------------------APLICATION MENU------------------------------------"""


class EnterMenuStrategy(BaseMenuStrategy):
    menu_class = EnterMenu


class BaseAplicationMenuStrategy(BaseMenuStrategy):
    menu_class = None

    def eventListen(self, event):
        super().eventListen(event)
        self.aplication.controller.back(event)
        return


class SettingsMenuStrategy(BaseAplicationMenuStrategy):
    menu_class = SettingsMenu


class LevelManagerStrategy(BaseAplicationMenuStrategy):
    menu_class = LevelManagerMenu


"""----------------------------GAME COMPONENTS MENU------------------------------------"""


class InventoryStrategy(BaseMenuStrategy):
    menu_class = InventoryMenu

    def eventListen(self, event):
        super().eventListen(event)
        self.aplication.controller.showInventory(event)


"""----------------------------APLICATION------------------------------------"""

# The main class of the game


class Aplication:
    controller = None
    controleRealization = {
        KeyboardControle.name: KeyboardControle,
        JoystickControle.name: JoystickControle
    }
    controleRealizationIndex = 0
    menuStrategy: BaseStrategy
    gameStrategy: BaseStrategy
    dieMenuStrategy: BaseStrategy
    winMenuStrategy: BaseStrategy
    guiMenuStrategy: BaseStrategy
    settingsMenuStrategy: BaseStrategy
    inventoryStrategy: BaseStrategy
    levelManagerStrategy: BaseStrategy

    _actingStrategy = None

    isMenu = False
    isPlayerDie = False
    isInventory = False
    isSettings = False
    isFPS = True
    _lastStrategy = None
    __run = True
    ticks = 0

    def __init__(self, controllerType: str = 'keyboard', *args, **kwargs):
        self.onStart(controllerType)

    def onStart(self, controllerType, *args, **kwargs):  # 1
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

        self.groups = Groups
        self.player = self.createPlayer()
        self.levelManager = LevelManager(self, self.groups)

        self.createStrategies()

    def onCreateGame(self):  # 2
        self.groups.Interface.add(EquipmentDrawer(self.player.equipment))
        self.levelManager.SetLevel("Level1")
        self.levelManager.Start()
        self._actingStrategy = self.gameStrategy

    def onRestartGame(self):  # 3
        self.game_timer.reset()
        self.player.restart()
        self.createStrategies()
        self.groups.restart()
        self.levelManager.Restart()
        self.levelManager.Start()
        self.groups.Interface.add(EquipmentDrawer(self.player.equipment))
        self.showMenu(value=False)

    def onQuitGame(self):  # 4
        self.game_timer.reset()
        self.createStrategies()
        self.levelManager.Reset()
        self.groups.restart()
        self.player.restart()
        self.isPlayerDie = False

    def onClose(self):  # 5
        log.info('close app')
        self.__run = False
        self.onQuitGame()
        pg.quit()
        sys.exit()

    def createStrategies(self):
        self.menuStrategy = MenuStrategy(self)
        self.dieMenuStrategy = DieMenuStrategy(self)
        self.gameStrategy = GameStrategy(self)
        self.guiMenuStrategy = EnterMenuStrategy(self)
        self.winMenuStrategy = WinMenuStrategy(self)
        self.settingsMenuStrategy = SettingsMenuStrategy(self)
        self.inventoryStrategy = InventoryStrategy(self)
        self.levelManagerStrategy = LevelManagerStrategy(self)

        self._actingStrategy = self.guiMenuStrategy
        self._lastStrategy = self._actingStrategy

    def start(self):
        """main aplicatiodn start function"""
        log.info('start app')
        fontFPS = Text((self.display_size[0]*0.9, 20), str(
            int(self.clock.get_fps())),  (0, 255, 26), SysFont("hooge0553", 36), False)

        while self.__run:

            for event in pg.event.get():
                self._actingStrategy.eventListen(event)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        print(self.player.equipment._ultimate)

            self._actingStrategy.update()
            self._actingStrategy.draw(self.display)

            if self.isFPS:
                self.drawFPS(fontFPS)

            pg.display.update()
            self.clock.tick(90)

    def createPlayer(self):
        return Player(self.display_size,
                      self.groups.playerShell, self.groups.Particles)

    def drawFPS(self, text: Text):
        text.draw(self.display)
        fps = str(int(self.clock.get_fps()))
        if fps != text.text:
            text.updateText(text=str(int(self.clock.get_fps())))

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
            f"level <{self.levelManager.GetActingLevel().__class__.__name__}> was completed")

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

    def showInventory(self, value: bool = None):
        if self._actingStrategy == self.inventoryStrategy:
            self._actingStrategy = self._lastStrategy
        else:
            self._lastStrategy = self._actingStrategy
            self._actingStrategy = self.inventoryStrategy

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

    def showLevelManager(self, value: bool = None):
        if self._actingStrategy == self.levelManagerStrategy:
            self._actingStrategy = self._lastStrategy
        else:
            self._lastStrategy = self._actingStrategy
            self._actingStrategy = self.levelManagerStrategy

    def showSettings(self, value: bool = None):
        log.debug('show settings')

        if self._actingStrategy == self.settingsMenuStrategy:
            self._actingStrategy = self._lastStrategy
        else:
            self._lastStrategy = self._actingStrategy
            self._actingStrategy = self.settingsMenuStrategy

    def backToLastStrategy(self):
        self._actingStrategy = self._lastStrategy

    def leaveToMenu(self):
        self._actingStrategy = self.guiMenuStrategy
        self.onQuitGame()

    def changeLevel(self, name: str):
        self.groups.Background.empty()
        self.levelManager.SetLevel(name)


if __name__ == '__main__':
    import logger
    pg.init()
    pg.font.init()
    log = logger.setup_logger()
    aplication = Aplication()
    aplication.start()
