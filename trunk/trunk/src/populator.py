import os
import copy
from ai import *
from item import *

class Populator(object):
    
    game = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def fill_items(map, filename, min, max):
        stuff = open(os.path.join('item', filename + '.pdcif'), 'r').read()
        stuff = stuff.split('\n')
       
        items = Populator.findAll(stuff)
        
        for _ in xrange(min, max):
            name = random.choice(items)
            item = Populator.create_item(name, stuff)
            item.set_pos(Populator.game.map.get_random_pos())
            Populator.game.items.append(item)
            
    @staticmethod
    def fill_creatures(map, filename, min, max):
        creatures = open(os.path.join('npc', filename + '.pdccf'), 'r').read()
        creatures = creatures.split('\n')
       
        actors = Populator.findAll(creatures)
        
        for _ in xrange(min, max):
            name = random.choice(actors)
            actor = Populator.create_actor(name, creatures)
            actor.set_pos(Populator.game.map.get_random_pos())
            Populator.game.actors.append(actor)

    @staticmethod
    def create_item(name, stuff):
        i = None
        
        sn = True
        br = False
        for index in xrange(0, len(stuff)):
            if not br:
                line = stuff[index]
                if line.strip() == '': continue
                
                if sn:
                    if line[1:] == name:
                        i = Item(False)
                        sn = False
                        continue
                else:
                    if line[0] == '*':
                        br = True
                        continue
                    
                    attr = line.split('=')[0]
                    value = line.split('=')[1]
                    
                    if attr == 'type':
                        i.type =  globals()[value]
                    elif attr == 'eq_img':
                        i.eq_img = int(value.split(',')[0]),int(value.split(',')[1])
                    elif attr == 'dd_img':
                        i.dd_img = int(value)
                    elif attr == 'dv':
                        i.dv = int(value)
                    elif attr == 'av':
                        i.av = int(value)
                    elif attr == 'min_damage':
                        i.min_damage = int(value)
                    elif attr == 'max_damage':
                        i.max_damage = int(value)
                    elif attr == 'name':
                        i.name = value
                    elif attr == 'flags':
                        flags = value.split(',')
                        for flag in flags:
                            i.flags |= globals()[flag] #that's why i love python :)
        return i
    
    @staticmethod
    def create_actor(name, stuff):
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
