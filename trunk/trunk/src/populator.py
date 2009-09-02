import os
import copy
from ai import *
from configuration import Configuration

class Populator(object):
    
    game = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def fill(map, filename, min, max):
        stuff = open(os.path.join('npc', filename + '.pdccf'), 'r').read()
        stuff = stuff.split('\n')
       
        actors = Populator.findAll(stuff)
        
        for _ in xrange(min, max):
            name = random.choice(actors)
            actor = Populator.create(name, stuff)
            Populator.game.actors.append(actor)
    
    @staticmethod
    def create(name, stuff):
        a = None
        
        sn = True
        br = False
        for index in xrange(0, len(stuff)):
            if not br:
                line = stuff[index]
                if line.strip() == '': continue
                
                if sn:
                    if line[1:] == name:
                        a = Actor(False)
                        a.set_pos(Populator.game.map.get_random_pos())
                        sn = False
                        continue
                else:
                    
                    if line[0] == '*':
                        br = True
                        continue
                    
                    attr = line.split('=')[0]
                    value = line.split('=')[1]
                    
                    if attr == 'image':
                        a.img_body = int(value), 0
                    elif attr == 'speed':
                        a.speed = a.cur_speed = int(value)
                    elif attr == 'ai':
                        ai_class = globals()[value]
                        a.ai = ai_class(a)
                    elif attr == 'name':
                        a.name = value
                    elif attr == 'natural_av':
                        a.natural_av = int(value)

        return a
    
    @staticmethod
    def findAll(stuff):
        actors = []
        for line in stuff:
            if line.strip() == '': continue
            if line[0] == '*':
                actors.append(line[1:])
        return actors
