from pdcresource import *
from pdcglobal import *
from magic import Spell

class ColdSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = BLUE
        self.type = ST_GENERIC
        
class FrostRay(ColdSpell):
    def __init__(self):
        ColdSpell.__init__(self)
        self.phys_cost = 15
        self.mind_cost = 30
        self.name = 'Frost Ray'
        self.infotext = 'Damage Foes with cold'

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
            self.game.do_damage(target, amount, D_COLD)
            self.game.shout('%s freezed %s' % (self.caster.name, target.name))
        self.game.wait_for_target = None
        self.game.state = S_RUN