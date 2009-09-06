class Effect(object):
    def __init__(self, duration, host):
        self.duration = duration
        self.host = host
        host.fx.append(self)
        
    def tick(self):
        self.duration -= 1
        if self.duration == 0:
            self.host.fx.remove(self)
        
