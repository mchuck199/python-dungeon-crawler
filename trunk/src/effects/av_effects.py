from pdcglobal import *
from effect import Effect

class StunEffect(Effect):
    def __init__(self, host,owner):
        dur = d(3)
        Effect.__init__(self, dur, host,owner)
    
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
        self.host.game.do_damage(self.host, d(3))
        if self.host == self.host.game.player:
            self.host.game.shout('You are bleeding')
        else:
            self.host.game.shout('%s bleeds' % (self.host.name))
        Effect.tick(self)
        
class StrokingEffect(Effect):
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
    
    def tick(self):
        if self.host == self.host.game.player:
            self.host.game.shout('You are getting stroked by %s'%(self.owner))
        else:
            self.host.game.shout('%s is getting stroked' % (self.host.name))
        Effect.tick(self)