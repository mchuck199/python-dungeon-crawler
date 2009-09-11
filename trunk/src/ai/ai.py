from key_mapping import *
from pdcresource import *
from pdcglobal import *
from actor import Actor
from shadowcast import sc

class AI(object):
    game = None
    def __init__(self, actor):
        self.actor = actor
        self.hostile = []
        self.sc = sc(self.game.map.map_array)
        
    def act(self):
        pass

    def seeing_player(self):
        dis = get_dis(self.actor.x, self.actor.y, self.game.player.x, self.game.player.y)
        if dis > 15:
            return False
        
        self.sc.do_fov(self.actor.x, self.actor.y, self.actor.cur_mind / 20 + 7)
        x, y = self.game.player.pos()
        return self.sc.lit(x, y)
        
#        blocked = False
#        fields = line(self.actor.x, self.actor.y, self.game.player.x, self.game.player.y)
#        for f in fields:
#            x, y = f
#            blocked |= self.game.map.map_array[y][x][MT_FLAGS] & F_BLOCKSIGHT
#        return not blocked    
    
    def get_player_direction(self):
        return self.actor.locateDirection(self.game.player)
    
    def build_alternate_dirs(self, dir, panic=False):
        if dir == MOVE_UP: return [MOVE_UP_LEFT, MOVE_UP_RIGHT] if not panic else [MOVE_UP_LEFT, MOVE_UP_RIGHT, MOVE_RIGHT, MOVE_LEFT] 
        if dir == MOVE_DOWN: return [MOVE_DOWN_LEFT, MOVE_DOWN_RIGHT]if not panic else [MOVE_DOWN_LEFT, MOVE_DOWN_RIGHT, MOVE_RIGHT, MOVE_LEFT]
        if dir == MOVE_LEFT: return [MOVE_UP_LEFT, MOVE_DOWN_LEFT]if not panic else [MOVE_UP_LEFT, MOVE_UP_RIGHT, MOVE_UP, MOVE_DOWN]
        if dir == MOVE_RIGHT:return [MOVE_UP_RIGHT, MOVE_DOWN_RIGHT]if not panic else [MOVE_UP_RIGHT, MOVE_DOWN_RIGHT, MOVE_UP, MOVE_DOWN]
        if dir == MOVE_WAIT:return []
        if dir == MOVE_UP_LEFT:return [MOVE_LEFT, MOVE_UP]if not panic else [MOVE_LEFT, MOVE_UP, MOVE_UP_RIGHT, MOVE_DOWN_LEFT]
        if dir == MOVE_DOWN_LEFT:return [MOVE_DOWN, MOVE_LEFT]if not panic else [MOVE_DOWN, MOVE_LEFT, MOVE_UP_LEFT, MOVE_DOWN_RIGHT]
        if dir == MOVE_UP_RIGHT:return [MOVE_UP, MOVE_RIGHT]if not panic else [MOVE_UP, MOVE_RIGHT, MOVE_UP_LEFT, MOVE_DOWN_RIGHT]
        if dir == MOVE_DOWN_RIGHT:return [MOVE_DOWN, MOVE_RIGHT]if not panic else [MOVE_DOWN, MOVE_RIGHT, MOVE_DOWN_LEFT, MOVE_UP_RIGHT]
    
    def move_randomly(self):
        list = []
        
        if d(20) < 10:
            self.actor.move(MOVE_WAIT)
        
        for item in MOVES:
            list.append(item)
            
        random.shuffle(list)
        success = False
        while len(list) > 0 and not success:
            dir = list.pop()
            new_pos = get_new_pos(self.actor.pos(), dir)
            act = self.game.get_actor_at(new_pos)
            if act != None:
                if act not in self.hostile:
                    continue
            success = self.actor.move(dir)

