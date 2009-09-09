from pdcglobal import *
from item import Item

class Armor(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_ARMOR
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']
        
class Cloak(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_ARMOR

    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']
        
class Weapon(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_WEAPON
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']
        
class Shield(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_SHIELD
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']

class Boots(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_BOOTS
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']

class Helmet(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_HELMET
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']

class Gold(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_GOLD
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']

class Stuff(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_STUFF
        
    def into(self):
        if self.flags & IF_IDENTIFIED:
            return ['dam: %i-%i av: %i' % (self.min_damage, self.max_damage, self.av)]
        else:
            return ['not identified']
        

        

        
