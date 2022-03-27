from typing import Tuple, List
from pygame.sprite import AbstractGroup
from GameObjects.weapons import RocketLauncher, LiteGun, BurnedLauncher, IWeapon
from GameObjects.ultimates import IUltimate, Striker, InvisibleEffectSender
# -----------------------------


class Equipment:
    def __init__(self, group: AbstractGroup, particle_group: AbstractGroup):
        self._group = group
        self._particle_group = particle_group

        self.weaponIndex = 0
        self._weapon_equipment: List[IWeapon] = []
        self._heal_equipment = []
        self._ultimate: IUltimate = None
        self.isUltimateSelected = False

        self.AddWeapon(LiteGun, RocketLauncher, BurnedLauncher)
        # self.AddUltimate(Striker)
        self.AddUltimate(InvisibleEffectSender)

    def BoolSelectUltimate(self):
        """set isUltimateSelected - True"""
        self.isUltimateSelected = True

    def BoolDiselectUltimate(self):
        """set isUltimateSelected - False"""
        self.isUltimateSelected = False

    def SelectUltimate(self, player_instance):
        if self._ultimate.isSelectable:
            self.isUltimateSelected = not self.isUltimateSelected
            self._ultimate.Select(self.isUltimateSelected, player_instance)

    def SelectWeapon(self):
        pass

    def SelectObject(self, update=None, value=None):
        if self.isUltimateSelected:
            self.isUltimateSelected = False
            self._ultimate.Select(isUsed=self.isUltimateSelected)

        if value:
            if 0 <= value-1 <= len(self._weapon_equipment)-1:
                self.weaponIndex = value - 1
        elif update:
            if 0 <= update+self.weaponIndex <= len(self._weapon_equipment)-1:
                self.weaponIndex += update
            elif update+self.weaponIndex < 0:
                self.weaponIndex = len(self._weapon_equipment)-1
            elif update+self.weaponIndex > len(self._weapon_equipment)-1:
                self.weaponIndex = 0

    def UseWeapon(self, rect, *args, **kwargs):
        self._weapon_equipment[self.weaponIndex].Use(rect)

    def UseUltimate(self, player_instance):
        self._ultimate.Use(player_instance)

    def UseObject(self, rect, *args, **kwargs):
        if self.isUltimateSelected:
            return self.UseUltimate()

        return self.UseWeapon(rect, *args, **kwargs)

    def AddWeapon(self, *prefabs: Tuple[IWeapon]):
        for prefab in prefabs:
            self._weapon_equipment.append(
                prefab(group=self._group, particle_group=self._particle_group))

    def AddUltimate(self, prefabs: IUltimate):
        self._ultimate = prefabs(
            group=self._group, particle_group=self._particle_group, BoolDeselectFunc=self.BoolDiselectUltimate)

    def countWeapons(self):
        return len(self._weapon_equipment)
