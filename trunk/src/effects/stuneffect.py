from pdcglobal import *
from effect import Effect

class StunEffect(Effect):
    def __init__(self, host):
        dur = d(3)
        Effect.__init__(self, dur, host)
    
    def tick(self):
        self.host.timer += self.host.speed * d(3)
        self.host.game.message_queue.insert(0,'%s is stunned'%(self.host.name))
        Effect.tick(self)