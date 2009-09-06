from key_mapping import *
from pdcresource import *
from pdcglobal import *
from actor import Actor
from ai import AI

class ChasePlayerAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor)

    def act(self):
        if not self.seeing_player():
            self.move_randomly()
        else:
            player_dir = self.get_player_direction()
            alt_dirs = self.build_alternate_dirs(player_dir)
            success = False
            
            move = self.actor.move(player_dir)
            
            if move == True:
                return
            
            if not move or not isinstance(move, Actor):
                for d in alt_dirs:
                    success = self.actor.move(d)
                    if success or isinstance(success, Actor): 
                        break
            else:
                success=True
            
            if not success and not isinstance(success, Actor):
                self.move_randomly()
