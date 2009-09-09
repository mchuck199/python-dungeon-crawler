class Effect(object):
    def __init__(self, duration, host, owner):
        self.duration = duration
        self.host = host
        self.owner = owner
        host.running_fx.append(self)
        
    def tick(self):
        self.duration -= 1
        if self.duration == 0:
            self.host.running_fx.remove(self)
        
