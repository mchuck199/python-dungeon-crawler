import random

class Room(object):
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.room = []
        for _ in xrange(self.height):
            line = []
            for _ in xrange(self.width):
                line.append(1)
            self.room.append(line)
        
        self.childs = []
    
    def split(self):
        h = random.choice([True, False])
        if h:
            
            s_x = random.randint(2, self.width - 2)
            r1 = Room(s_x, self.height)
            r2 = Room(self.width - s_x, self.height)
        else:
            s_y = random.randint(2, self.height - 2)
            r1 = Room(self.width, s_y)
            r2 = Room(self.width, self.height - s_y)
            
        self.childs.append(r1)
        self.childs.append(r2)
        
    def printme(self):
        if len(self.childs) == 0:
            print 'room:'
            for line in self.room:
                print line
        else:

            for c in self.childs:
                c.printme()


def start(x, y):
    r = Room(x, y)
    r.split()
    for c in r.childs:
        c.split()
        for c1 in c.childs:
            c1.split    
           
    r.printme()
        
        
if __name__ == '__main__':
    start(25, 25)
