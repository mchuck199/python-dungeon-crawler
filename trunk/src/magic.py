from pdcresource import *
from pdcglobal import *

class Spell(object):
    
    game = None
    
    def __init(self):
        self.phys_cost = 10
        self.mind_cost = 25
        self.name = 'generic'
        self.infotext = 'nothing'
        self.color = WHITE
        
    def cast(self, caster):
        pass
    
    def info(self):
        return 'PHY: %i MND: %i - %s' % (self.phys_cost, self.mind_cost, self.infotext)

class Identify(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.phys_cost = 0
        self.mind_cost = 30
        self.name = 'Identify'
        self.infotext = 'Identify an Item'
        self.color = GREEN
    def cast(self, caster):
        self.game.player_actions.identify()
    
class LesserHealing(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.phys_cost = 10
        self.mind_cost = 25
        self.name = 'Lesser Healing'
        self.infotext = 'Healing'
        self.color = WHITE
    def cast(self, caster):
        amount = d(10) + 1
        if caster.cur_health + amount > caster.health:
            amount = caster.health - caster.cur_health
        self.game.do_damage(caster, -amount)

class MajorHealing(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.phys_cost = 25
        self.mind_cost = 55
        self.name = 'Healing'
        self.infotext = 'nothing'
        self.color = WHITE
    def cast(self, caster):
        amount = d(10) + d(10) + 5
        self.game.do_damage(caster, -amount)

class LesserHaste(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.phys_cost = 15
        self.mind_cost = 15
        self.name = 'Lesser Haste'
        self.infotext = 'Speed Up'
        self.color = BLUE
    def cast(self, caster):
        amount = d(10) + d(10) + 2
        if caster.cur_speed > caster.speed / 2:
            caster.cur_speed -= amount
