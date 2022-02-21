from typing import List, Tuple
from level.levels import *
from logger import get_logger
log = get_logger(__name__)


def HasActingLevel(func):
    def wrapper(self, *args, **kwargs):
        if self._actingObject is not None:
            return func(self, *args, **kwargs)
        log.error("_actingObject is none")
        return None

    return wrapper


class LevelManager:
    _list: List[BaseLevel] = []
    _actingObject: BaseLevel = None

    def __init__(self, aplication, groups):
        self.aplication = aplication
        self.groups = groups
        self.AddLevel(Level1, AsteroidWaves)

    def SetLevel(self, name: str):
        _obj = self.GetLevel(name=name)
        if _obj is not None:
            self._actingObject = _obj

    def AddLevel(self, *levels: Tuple[BaseLevel]):
        for level in levels:
            self._list.append(level(self.aplication, self.groups))

    def GetLevel(self, name: str):
        filtered_list = list(
            filter(lambda lv: lv.__class__.__name__ == name, self._list))
        if len(filtered_list) > 0:
            return filtered_list[0]
        log.error(f"level '{name}' not found")
        raise ValueError

    def GetActingLevel(self):
        return self._actingObject

    @HasActingLevel
    def Update(self, *args,  **kwargs):
        self.GetActingLevel().update(*args,  **kwargs)

    @HasActingLevel
    def Restart(self, *args, **kwargs):
        self.GetActingLevel().restart(*args, **kwargs)

    def Reset(self):
        self._actingObject = None

    @HasActingLevel
    def Start(self, *args, **kwargs):
        self.GetActingLevel().start(*args, **kwargs)
