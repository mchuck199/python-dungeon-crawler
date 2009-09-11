import dungeon
import magic

class Class(object):
    def __init__(self,host):
        self.host=host

class Fighter(Class):
    desc='Thanks to unremittingly training, $$$ was skilled at all weapons.'
    def __init__(self,host):
        Class.__init__(self,host)
        i = dungeon.Populator.create_item('Flail', 'basic_weapons', 2)
        self.host.items.append(i)
        #self.host.equip(i)
        
        c = dungeon.Populator.create_item('Chainmail', 'basic_stuff', 2)
        self.host.items.append(c)
        self.host.equip(c)

        b = dungeon.Populator.create_item('Bow','basic_weapons',0)
        self.host.items.append(b)
        self.host.equip(b)
        
        r = dungeon.Populator.create_item('Arrows','basic_weapons',0)
        self.host.items.append(r)
        self.host.equip(r)
        
        if hasattr(self.host.slot,'trousers'):
            t = dungeon.Populator.create_item('Trousers', 'basic_stuff', 2)
            self.host.items.append(t)
            self.host.equip(t)
        
class Barbarian(Class):
    desc='Since his youth, $$$ clearly loved one weapon the most: the Axe.'
    def __init__(self,host):
        Class.__init__(self,host)
        i = dungeon.Populator.create_item('Axe', 'basic_weapons', 2)
        self.host.items.append(i)
        self.host.equip(i)
        
        if hasattr(self.host.slot,'trousers'):
            t = dungeon.Populator.create_item('Trousers', 'basic_stuff', 2)
            self.host.items.append(t)
            self.host.equip(t)
        
class Priest(Class):
    desc='Since %%% birth, $$$ stood up for Law and Order.'
    def __init__(self,host):
        Class.__init__(self,host)   
        
         
class Sorcerer(Class):
    desc='All %%% live $$$ tried to master the Elemental-Forces '
    def __init__(self,host):
        Class.__init__(self,host)
        self.host.spells.append(magic.fire_spells.FireBall())
        
class Necromancer(Class):
    desc='Allured by the Power of Chaos, $$$ was a fearsome Wizrad.'  
    def __init__(self,host):
        Class.__init__(self,host)
        
classkits = (('Fighter',Fighter),
             ('Barbarian',Barbarian),
             ('Sorcerer',Sorcerer),
             ('Priest',Priest),
             ('Necromancer',Necromancer))