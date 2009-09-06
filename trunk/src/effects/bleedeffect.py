from pdcglobal import *
from effect import Effect

class BleedEffect(Effect):
    def __init__(self, host):
        dur = d(10)
        Effect.__init__(self, dur, host)
    
    def tick(self):
        self.host.game.do_damage(self.host,d(3))
        self.host.game.message_queue.insert(0,'%s bleeds'%(self.host.name))
        Effect.tick(self)