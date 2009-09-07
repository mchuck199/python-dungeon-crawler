from pdcglobal import *
from effect import Effect
from dv_effects import DazzleEffect

class StunEffect(Effect):
    def __init__(self, host, owner):
        dur = d(3)
        Effect.__init__(self, dur, host, owner)
    
    def tick(self):
        self.host.timer += self.host.speed * d(3)
        if self.host == self.host.game.player:
            self.host.game.shout('You are stunned')
        else:
            self.host.game.shout('%s is stunned' % (self.host.name))
        
        Effect.tick(self)

class BleedEffect(Effect):
    def __init__(self, host, owner):
        dur = d(10)
        Effect.__init__(self, dur, host, owner)
    
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_GENERIC)
        if self.host == self.host.game.player:
            self.host.game.shout('You are bleeding')
        else:
            self.host.game.shout('%s bleeds' % (self.host.name))
        Effect.tick(self)

class PoisonEffect(Effect):
    def __init__(self, host, owner):
        dur = d(10)
        Effect.__init__(self, dur, host, owner)
    
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_POISON)
        if d(100) < 35:
            StunEffect(self.host, self.owner)
        if d(100) < 35:
            DazzleEffect(self.host, self.owner)
        if self.host == self.host.game.player:
            self.host.game.shout('You are poisoned')
        else:
            self.host.game.shout('%s is poisoned' % (self.host.name))
        Effect.tick(self)
        
class StrokingEffect(Effect):
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
    
    def tick(self):
        if self.host == self.host.game.player:
            self.host.game.shout('You are getting stroked by %s' % (self.owner))
        else:
            self.host.game.shout('%s is getting stroked' % (self.host.name))
        Effect.tick(self)
