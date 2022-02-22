from typing import List, Tuple
from level.levels import *
from logger import get_logger
log = get_logger(__name__)


def HasActingLevel(func):
    """
    This is a decorator function that checks if the object has an acting object. If it does, it executes
    the function. If it doesn't, it throws an error

    :param func: The function that you want to wrap
    :return: A function that returns a function.
    """

    def wrapper(self, *args, **kwargs):
        if self._actingLevel is not None:
            return func(self, *args, **kwargs)
        log.error("_actingLevel is none")
        return None

    return wrapper


# The LevelManager need to use and manage levels
# Also It used to interact the acting level
class LevelManager:
    _levels: List[BaseLevel] = []
    _actingLevel: BaseLevel = None

    def __init__(self, aplication, groups):
        self.aplication = aplication
        self.groups = groups
        self.AddLevel(Level1, AsteroidWaves, StrikerField)

    def SetLevel(self, name: str):
        _obj = self.GetLevel(name=name)
        if _obj is not None:
            self._actingLevel = _obj

    def AddLevel(self, *levels: Tuple[BaseLevel]):
        for level in levels:
            self._levels.append(level(self.aplication, self.groups))

    def GetLevel(self, name: str):
        filtered_levels = list(
            filter(lambda lv: lv.__class__.__name__ == name, self._levels))
        if len(filtered_levels) > 0:
            return filtered_levels[0]
        log.error(f"level '{name}' not found")
        raise ValueError

    def GetActingLevel(self):
        return self._actingLevel

    @HasActingLevel
    def Update(self, *args,  **kwargs):
        self.GetActingLevel().update(*args,  **kwargs)

    @HasActingLevel
    def Restart(self, *args, **kwargs):
        self.GetActingLevel().restart(*args, **kwargs)

    def Reset(self):
        self._actingLevel = None

    @HasActingLevel
    def Start(self, *args, **kwargs):
        self.GetActingLevel().start(*args, **kwargs)
