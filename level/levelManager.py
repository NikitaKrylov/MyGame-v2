from typing import List, Tuple
import pygame as pg
from level.levels import *


class LevelManager:
    def __init__(self):
        self._list: List[BaseLevel] = []
        self.actingIndex:int = None
        self.actingObject:BaseLevel = None
        self.AddLevel(Level1, AsteroidWaves)
        
    def ChangeLevel(self, index:int=None, name:str=None):
        _obj = None
        if index is not None or name is not None:
            _obj = self.GetLevel(index=index, name=name)

            if _obj is not None:
                self.actingObject = _obj
                self.actingIndex = self._list.index(_obj)


    def AddLevel(self, *levels: Tuple[BaseLevel]):
        for level in levels:
            self._list.append(level)

    def GetLevel(self, index:int=None, name:str=None):
        if index is not None:
            return self._list[index] if 0 < index < len(self._list)-1 else None

        if name is not None:
            return self._list.sort(key=lambda lv: lv.__class__.__name__ == name)
        
    def GetActingLevel(self):
        return (self.actingIndex, self.actingObject)

    def Update(self, *args,  **kwargs):
        index, _obj = self.GetActingLevel()
        _obj.update(*args,  **kwargs)
        
    def Restart(self):
        index, _obj = self.GetActingLevel()
        _obj.restart()
        
    def Start(self):
        index, _obj = self.GetActingLevel()
        _obj.start()
