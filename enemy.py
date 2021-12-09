from exception import NoneInitializeError
from animation import Animator
import pygame as pg
from pygame.sprite import Sprite

class AbstractEnemy(Sprite):  # Sprite Interface
    name = 'EnemyName'
    XP = 1000
    animation = Animator
    ability = None

    def __init__(self, *args, **kwargs):
        super().__init__()

    def updatePosition(self):
        return

    def updateAnimation(self):
        pass

    def update(self, *args, **kwargs):
        print(self.__str__() + ' was updated')

    def draw(self):
        print(self.__str__() + ' was drown')

    def kill(self):
        self.name = f'#{self.name}#'
        return 'Объект ' + self.name + ' уничтожен'

    def getDamage(self, objects):  # ->damage received, remaining HP
        pass

    def toDamage(self):
        pass

    def __str__(self):
        return self.name


class FirstEnemy(AbstractEnemy): # Sprite 
    name = 'FirstEnemy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SecondEnemy(AbstractEnemy): # Sprite 
    name = 'SecondEnemy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def shot(self):
        return self.name + '-> Другой выстрел*'


class ThirdEnemy(SecondEnemy):# Sprite
    name = 'ThirdEnemy'
    XP = 3500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# -----------------------------------------------------------------

class AbstarctFactory:
    __object = None

    def __init__(self, group=None, object=None, *args, **kwargs):
        self.setGroup(group)
            
        if object:
            self.setObject(object)


    def createObject(self, *args, **kwargs):  # -> Object type of object
        if self.__object:
            _object = self.__object(*args, **kwargs)
            self.__addToGroup(_object)
            return _object
        raise NoneInitializeError('self.__object')

    def __addToGroup(self, object):  # -> Group
        self.__group.append(object)
        return self.__group
        

    def count(self):  # -> int
        return len(self.__group)

    @property
    def getGroup(self):
        return self.__group

    def getObjectClasss(self):
        return self.__object

    def setGroup(self, group):
        self.__group = group
        return self.__group
    
    def setObject(self, object):
        self.__object = object
        return self.__object
    
    def update(self):
        for obj in self.getGroup:
            obj.update()

    def updateAllObjectCondition(self, func):
        """apply fuction to all gropu object 
        for example, change damage
        """
        pass

    def __destroyAllObject(self):
        pass


# ------------------------------------------------------------------



class FirstEnemyFactory(AbstarctFactory):
    __object = FirstEnemy
    __group = []
    
    def __init__(self, group=None, object=None, *args, **kwargs):
        super().__init__(group=self.__group, object=self.__object, *args, **kwargs)

    def createEnemy(self, *args, **kwargs):
        return super().createObject(*args, **kwargs)


class SecondEnemyFactory(AbstarctFactory):
    __object = SecondEnemy
    __group = []
    
    def __init__(self, group=None, object=None, *args, **kwargs):
        super().__init__(group=self.__group, object=self.__object, *args, **kwargs)

    def createEnemy(self, *args, **kwargs):
        return super().createObject(*args, **kwargs)


class ThirdEnemyFactory(AbstarctFactory):
    __object = ThirdEnemy
    __group = []
    
    def __init__(self, group=None, object=None, *args, **kwargs):
        super().__init__(group=self.__group, object=self.__object, *args, **kwargs)

    def createEnemy(self, *args, **kwargs):
        return super().createObject(*args, **kwargs)
