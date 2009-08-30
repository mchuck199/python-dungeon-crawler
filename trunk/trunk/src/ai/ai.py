from key_mapping import *
from pdcresource import *
from pdcglobal import *
from actor import Actor

class AI(object):
    game = None
    def __init__(self, actor):
        self.actor = actor
        
    def act(self):
        pass

    def seeing_player(self):
        blocked=False
        fields = line(self.actor.x, self.actor.y, self.game.player.x, self.game.player.y)
        for f in fields:
            x, y = f
            blocked |= self.game.map.map_array[y][x][MT_FLAGS] & F_BLOCKSIGHT
        return not blocked    
    
    def get_player_direction(self):
        return self.actor.locateDirection(self.game.player)
    
    def move_randomly(self):
        list = []
        for item in MOVES:
            list.append(item)
            
        random.shuffle(list)
        success = False
        while len(list) > 0 and not success:
            dir = list.pop()
            success = self.actor.move(dir)

