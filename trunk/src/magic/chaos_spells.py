from pdcresource import *
from pdcglobal import *
from magic import Spell

class ChaosSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = PURPLE
        self.type = ST_GENERIC
        
class FoulnessRay(ChaosSpell):
    def __init__(self):
        ChaosSpell.__init__(self)
        self.phys_cost = 10
        self.mind_cost = 5
        self.name = 'Ray of Foulness'
        self.infotext = 'Damage Foes with Chaos'
    def cast(self, caster):
        self.caster = caster
        self.game.wait_for_target = self
        self.game.player_actions.cursor()
    def target_choosen(self, pos):
        target = self.get_ray_target(self.caster.pos(), pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            amount = d(self.caster.mind / 20) + self.caster.mind / 20
            self.game.do_damage(self.caster, amount / 2, D_CHAOS)
            self.game.do_damage(target, amount, D_CHAOS)
            self.game.shout('%s befouled %s' % (self.caster.name, target.name))
        self.game.wait_for_target = None
        self.game.state = S_RUN