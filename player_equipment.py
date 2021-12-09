from animation import Animator
from shell import FirstShell

class ObjectInterface:
    # def __init__(self, group):
    #     self.group = group
        
    def getDiscription(self):
        return 'some discription'
    
    def execute(self):
        pass


class AbstractWeapon(ObjectInterface):
    pass


class AbstractGun(AbstractWeapon):
    amo = FirstShell
    
    def strike(self):
        _shell = self.amo()
        return _shell



class AbstractUltimate(ObjectInterface):
    pass


class AbstractHeal(ObjectInterface):
    pass



# -------------------------------------------------------------------

class Equipment:
    _weapon_equipment = [] #Weapons
    _heal_equipment = [] #Heals
    _ultimate = None #Ultimates

    def useUltimate(self):
        self._ultimate.use()

    def useWeapon(self):
        pass

    def useHeal(self):
        return

    def addWeapon(self, instance):
        self._weapon_equipment.append(instance)
        return self._weapon_equipment

    def addHeal(self, instance):
        self._heal_equipment.append(instance)
        return self._heal_equipment

    def setUltimate(self, instance):
        self._ultimate = instance
        return self._ultimate
