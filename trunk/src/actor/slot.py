from item import *

class Slot(object):
    def __init__(self, host):
        slots = {'cloak': Item(False),
                 'armor' : Item(False),
                 'boots' : Item(False),
                 'shield' : Item(False),
                 'weapon' : Item(False),
                 'head' : Item(False),
                 'ammo': Item(False),
                 'trousers':Item(False)}

        for slot in slots:
            self.__dict__[slot] = slots[slot]
        
        self.__dict__['slots'] = slots
        self.__dict__['host'] = host
    
    def __getstate__(self):
        return self.__dict__
  
    def __setstate__(self, state):
        for item in state:
            self.__dict__[item]=state[item]
    
    def __getattr__(self, attr):
        return self.__dict__[attr]

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
    
    def take_off(self, item):
        attr = item.__class__.__name__.lower()
        self.__dict__[attr] = Item(False)
        self.host.items.append(item)
        item.equipped = False
        
    def equip(self, item):
        
        attr = item.__class__.__name__.lower()
        
        if not hasattr(self,attr):
            self.host.game.shout('You can`t equip that')
            return False
            
        self.host.items.remove(item)
        old = self.__dict__[attr]
        self.__dict__[attr] = item

        item.equipped = True
        item.picked_up = True
         
        if not old.type == I_VOID:
            old.equipped = False
            self.host.items.append(old)
        return True
    def get_equipment(self):
        return [self.__dict__[slot] for slot in self.slots if not self.__dict__[slot].type == I_VOID]
    
    def clear_surfaces(self):
        for slot in self.slots:
            self.__dict__[slot].clear_surfaces()
