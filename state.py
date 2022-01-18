import pygame as pg
import sys
from menu import *


class BaseState:
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


class InventoryState(BaseState):
    def draw(self, display, *args, **kwargs):
        pass

    def update(self):
        pass

    def eventListen(self, event):
        return super().eventListen(event)


class GameState(BaseState):
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

        # print(self.aplication._actingState)
        if self.aplication.player.HP <= 0:
            self.aplication.showDieMenu(True)
            return

        self.aplication.level.update(now=_now)

        if self.aplication.level.isWin:
            self.aplication.setWinMenuState()

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


class BaseMenuState(BaseState):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = Menu(self.aplication, self.aplication.display_size)

    def draw(self, display):
        self.menu.draw(display)

    def eventListen(self, event):
        self.aplication.controller.menuUpdate(event)
        self.aplication.controller.menuExecute(event)
        return super().eventListen(event)


class MenuState(BaseMenuState):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = Menu(self.aplication, self.aplication.display_size)

    def eventListen(self, event):
        super().eventListen(event)
        self.aplication.controller.showMenu(event)
        return


class DieMenuState(BaseMenuState):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = DieMenu(mediator, mediator.display_size)


class WinMenuState(BaseMenuState):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = WinMenu(mediator, mediator.display_size)


class GUIMenuState(BaseMenuState):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.menu = AplicationMenu(mediator, mediator.display_size)


# ---------------------------------------------------------------------


class StateManager:
    menuState: BaseState = MenuState
    gameState: BaseState = GameState
    dieMenuState: BaseState = DieMenuState
    winMenuState: BaseState = WinMenuState
    guiMenuState: BaseState = GUIMenuState

    inventoryState: BaseState = None
    _actingState = None

    def __init__(self, mediator):
        self.mediator = mediator

        self.menuState = self.menuState(self.mediator)
        self.gameState = self.gameState(self.mediator)
        self.dieMenuState = self.dieMenuState(self.mediator)
        self.winMenuState = self.winMenuState(self.mediator)
        self.guiMenuState = self.guiMenuState(self.mediator)

        self.__actingState = self.guiMenuState

    @property
    def ActingState(self):
        return self.__actingState
