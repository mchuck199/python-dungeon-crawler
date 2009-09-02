class Camera(object):
    
    game = None
    
    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.x = 0
        self.y = 0
        self.edge = 7
        
    def adjust(self, x, y):
        #adjust to down
        if y - self.y > self.height - self.edge:
            self.y += 1
        #adjust to up
        if y - self.y < self.edge:
            self.y -= 1
            
        #adjust to right
        if x - self.x > self.width - self.edge:
            self.x += 1
        #adjust to up
        if x - self.x < self.edge:
            self.x -= 1
