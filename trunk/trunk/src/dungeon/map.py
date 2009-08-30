from pdcglobal import *
from pdcresource import Res
from dmap import *
import sys
import random
import copy
testmap = [
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, - 1, -1, -1, -1, -1, -1, -1, -1],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, - 1, -1, -1, -1, -1, -1, -1, -1],
         [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, - 1, -1, -1, -1, -1, -1, -1, -1],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, - 1, -1, -1, -1, -1, -1, -1, -1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, - 1, -1, -1, -1, -1, -1, -1, -1],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, - 1, -1, -1, -1, -1, -1, -1, -1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, - 1, -1, -1, -1, -1, -1, -1, -1]]


class Map(object):
    
    tiles = Res('dc-dngn.png', TILESIZE)
    game = None
    
    def __init__(self, MapArray):
        self.map_array = []
        
        
        for line in MapArray:
            new_line = []
            for tile in line:
                nt = (mt for mt in MAP_TILE_LIST if mt[MT_INDEX] == tile).next()
                new_line.append(copy.copy(nt))
            self.map_array.append(new_line)    
        
        self.height = len(MapArray)
        self.width = len(MapArray[0])
        self.cur_surf = None
        Debug.debug('Map is ' + str(self.width) + 'x' + str(self.height))
    
    @staticmethod
    def Random():
        startx = 80
        starty = 40
        somename = dMap()
        somename.makeMap(startx, starty, 110, 50, 60)
        array = [] 
        for y in range(0, starty):
            line = []
            for x in range(0, startx):
                if somename.mapArr[y][x] == 0: #floor
                    line.append(0)
                if somename.mapArr[y][x] == 1: #void
                    line.append(-1)
                if somename.mapArr[y][x] == 2: #wall
                    line.append(1)
                if somename.mapArr[y][x] == 3 or somename.mapArr[y][x] == 4 or somename.mapArr[y][x] == 5: #door
                    line.append(2)
            array.append(line)
        return Map(array)
    
    def get_random_pos(self):
        pos = None
        while pos == None:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            Debug.debug('get random pos: ' + str(x) + ' ' + str(y))
            if self.map_array[y][x][MT_FLAGS] & F_WALKABLE : pos = x, y
        return x, y
    
    def is_move_valid(self, old_pos, new_pos, move_mode):
        
        target_tile = self.map_array[new_pos[1]][new_pos[0]]
         
        #Debug.debug(str(target_tile))        
      
        if move_mode == MM_WALK and target_tile[MT_FLAGS] & F_WALKABLE: return True
        if move_mode == MM_FLY and target_tile[MT_FLAGS] & F_FLYABLE: return True
        if move_mode == MM_SWIM and target_tile[MT_FLAGS] & F_SWIMABLE: return True
                
        return False
        
    def get_tile_at(self, x, y):
        return self.tiles.get(self.map_array[y][x][MT_IMAGE])
