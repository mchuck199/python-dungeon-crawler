import random

class Gridbased(object):
    def __init__(self, height, width, mrs, cor):
        
        self.array = []
        [self.array.append([]) for _ in xrange(height)]
        [line.append(0) for _ in xrange(width) for line in self.array]
        self.cells = []
        
        y = 0
        cc = 0
        while y < height:
            while cc * mrs + cc < width:
                c = Cell((mrs * cc + cc, y),
                     (mrs * cc + cc + mrs, y),
                     (mrs * cc + 1 * cc, y + mrs),
                     (mrs * cc + cc + mrs, y + mrs))
                ul, ur, dl, dr = c.get()
                if dr[0] > width or dr[1] > height:
                    pass
                else:  
                    self.cells.append(c)
                
                cc += 1
            cc = 0
            y += mrs + 1
            
        for cell in self.cells:
            if random.randint(1, 100) < cor:
                cell.create_room()
                
        for cell in self.cells:
            if cell.room != None:
                ul, ur, dl, dr = cell.room.get()
                for y in xrange(ul[1] + 1, dl[1]):
                    for x in xrange(ul[0] + 1, ur[0]):
                        self.array[y][x] = 1
                        
                        
        for line in self.array:
            l = ''
            for c in line:
                l = l + str(c)
            print l
        
class Cell(object):
    def __init__(self, ul, ur, dl, dr):
        self.ul = ul
        self.ur = ur
        self.dl = dl
        self.dr = dr
        #print ul, ur, dl, dr
        self.room = None
    def get(self):
        return self.ul, self.ur, self.dl, self.dr
        
    def create_room(self):
        w = self.ur[0] - self.ul[0]
        rw = random.randint(5, w)
        rh = random.randint(5, w)
        xo = random.randint(0, 4)
        yo = random.randint(0, 4)
        self.room = Cell((self.ul[0] + xo, self.ul[1] + yo),
                         (self.ul[0] + rw, self.ul[1] + yo),
                         (self.ul[0] + xo, self.ul[1] + rh),
                         (self.ul[0] + rw, self.ul[1] + rh))
        #print self.room.get()
        
                       
                       
