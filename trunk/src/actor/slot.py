from item import *

class Slot(object):
    def __init__(self, host):
        self.host = host
        self.cloak = Item(False)
        self.armor = Item(False)
        self.boots = Item(False)
        self.shield = Item(False)
        self.weapon = Item(False)
        self.head = Item(False)
    
    def take_off(self, item):
        if isinstance(item, Armor):
            self.armor = Item(False)
        if isinstance(item, Boots):
            self.boots = Item(False)
        if isinstance(item, Cloak):
            self.cloak = Item(False)
        if isinstance(item, Helmet):
            self.head = Item(False)
        if isinstance(item, Shield):
            self.shield = Item(False)
        if isinstance(item, Weapon):
            self.weapon = Item(False)
        
        self.host.items.append(item)
        item.equipped = False
        
    def equip(self, item):
        self.host.items.remove(item)
        
        if isinstance(item, Armor):
            old = self.armor
            self.armor = item
        if isinstance(item, Boots):
            old = self.boots
            self.boots = item
        if isinstance(item, Cloak):
            old = self.cloak
            self.cloak = item
        if isinstance(item, Helmet):
            old = self.head
            self.head = item
        if isinstance(item, Shield):
            old = self.shield
            self.shield = item
        if isinstance(item, Weapon):
            old = self.weapon
            self.weapon = item
        
        item.equipped = True
         
        if not old.type == I_VOID:
            old.equipped = False
            self.host.items.append(old)
        
    def get_equipment(self):
        return [item for item in (self.cloak,
                                  self.armor,
                                  self.boots,
                                  self.weapon,
                                  self.shield,
                                  self.head) if not item.type == I_VOID]
    def clear_surfaces(self):
        self.cloak.clear_surfaces()
        self.armor.clear_surfaces()
        self.boots.clear_surfaces()
        self.weapon.clear_surfaces()
        self.shield.clear_surfaces()
        self.head.clear_surfaces()
