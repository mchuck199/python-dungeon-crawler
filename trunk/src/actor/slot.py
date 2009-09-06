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
    
    def take_off(self,item):
        if item.type == I_ARMOR:
            self.armor = Item(False)
        if item.type == I_BOOTS:
            self.boots = Item(False)
        if item.type == I_CLOAK:
            self.cloak = Item(False)
        if item.type == I_HELMET:
            self.head = Item(False)
        if item.type == I_SHIELD:
            self.shield = Item(False)
        if item.type == I_WEAPON:
            self.weapon = Item(False)
        
        self.host.items.append(item)
        item.equipped = False
        
    def equip(self, item):
        self.host.items.remove(item)
        
        if item.type == I_ARMOR:
            old = self.armor
            self.armor = item
        if item.type == I_BOOTS:
            old = self.boots
            self.boots = item
        if item.type == I_CLOAK:
            old = self.cloak
            self.cloak = item
        if item.type == I_HELMET:
            old = self.head
            self.head = item
        if item.type == I_SHIELD:
            old = self.shield
            self.shield = item
        if item.type == I_WEAPON:
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
