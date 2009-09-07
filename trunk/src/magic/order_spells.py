from pdcresource import *
from pdcglobal import *
from magic import Spell

class OrderSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = WHITE
        self.type = ST_ORDER

class LesserHealing(OrderSpell):
    def __init__(self):
        OrderSpell.__init__(self)
        self.phys_cost = 10
        self.mind_cost = 25
        self.name = 'Lesser Healing'
        self.infotext = 'Cures small wounds'
    
    def cast(self, caster):
        self.caster = caster
        self.game.wait_for_target = self
        self.game.player_actions.cursor()
    
    def target_choosen(self, pos):
        target = self.game.get_actor_at(pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            amount = d(self.caster.mind / 10) + 2
            if target.cur_health + amount > target.health:
                amount = target.health - target.cur_health
            self.game.do_damage(target, -amount)
            self.game.shout('%s healed %s' % (self.caster.name, target.name))
        self.game.wait_for_target = None
        self.game.state = S_RUN
        
class Healing(OrderSpell):
    def __init__(self):
        OrderSpell.__init__(self)
        self.phys_cost = 25
        self.mind_cost = 55
        self.name = 'Healing'
        self.infotext = 'Cures wounds'
   
    def cast(self, caster):
        self.caster = caster
        self.game.wait_for_target = self
        self.game.player_actions.cursor()
        
    def target_choosen(self, pos):
        target = self.game.get_actor_at(pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            amount = d(self.caster.mind / 10) + d(self.caster.mind / 10) + 5
            self.game.do_damage(target, -amount)
            self.game.shout('%s healed %s' % (self.caster.name, target.name))
        self.game.wait_for_target = None
        self.game.state = S_RUN
