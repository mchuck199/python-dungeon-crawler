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
            self.actor.move(self.get_player_direction())