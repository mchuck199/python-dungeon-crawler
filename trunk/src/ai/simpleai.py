from key_mapping import *
from pdcresource import *
from pdcglobal import *
from actor import Actor
from ai import AI

class SimpleAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor)
        
    def act(self):
        list=[]
        for item in MOVES:
            list.append(item)
            
        random.shuffle(list)
        success = False
        while len(list) > 0 and not success:
            dir = list.pop()
            success = self.actor.move(dir)