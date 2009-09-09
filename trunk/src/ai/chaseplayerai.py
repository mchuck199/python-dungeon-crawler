from key_mapping import *
from pdcresource import *
from pdcglobal import *
from actor import Actor
from ai import AI

class ChasePlayerAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor)
        self.hostile.append(self.game.player.id)

    def act(self):
        if not self.seeing_player():
            self.move_randomly()
        else:
            player_dir = self.get_player_direction()
            alt_dirs = self.build_alternate_dirs(player_dir)
            success = False
            
            act = self.game.get_actor_at(get_new_pos(self.actor.pos(), player_dir))
            if act != None:
                if act.id not in self.hostile:
                    self.actor.move(MOVE_WAIT)
                    return
                        
            move = self.actor.move(player_dir)
            
            if move == True:
                return
            
            if not move or not isinstance(move, Actor):
                for d in alt_dirs:
                    success = self.actor.move(d)
                    if success or isinstance(success, Actor): 
                        break
            else:
                success = True
            
            if not success and not isinstance(success, Actor):
                self.move_randomly()
