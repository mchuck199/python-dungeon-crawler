import os
import copy
import random
from ai import *
from item import *
from effects import *

class Populator(object):
    
    game = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def fill_map_with_items(map, filename, min, max, magic):
        stuff = open(os.path.join('item', filename + '.pdcif'), 'r').read()
        stuff = stuff.split('\n')
       
        items = Populator.findAll(stuff)
        
        for _ in xrange(min, max):
            name = random.choice(items)
            item = Populator.create_item(name, stuff, magic)
            item.set_pos(Populator.game.map.get_random_pos())
            Populator.game.items.append(item)
            
    @staticmethod
    def fill_map_with_creatures(map, filename, min, max):
        creatures = open(os.path.join('npc', filename + '.pdccf'), 'r').read()
        creatures = creatures.split('\n')
       
        actors = Populator.findAll(creatures)
        
        for _ in xrange(min, max):
            name = random.choice(actors)
            actor = Populator.create_actor(name, creatures)
            actor.set_pos(Populator.game.map.get_random_pos())
            Populator.game.actors.append(actor)

    @staticmethod
    def create_item(name, stuff, magic):
        item = None
        
        sn = True
        br = False
        for index in xrange(0, len(stuff)):
            if not br:
                line = stuff[index]
                if line.strip() == '': continue
                if line[0] == '#':continue
                
                if sn:
                    if line[1:] == name:
                        item = Item(False)
                        sn = False
                        continue
                else:
                    if line[0] == '*':
                        br = True
                        continue
                    
                    attr = line.split('=')[0]
                    value = line.split('=')[1]
                    
                    if attr == 'type':
                        item.type = globals()[value]
                    elif attr == 'img':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        eq, eq2, dd = pos[n].split(',')
                        item.eq_img = int(eq), int(eq2)
                        item.dd_img = int(dd)
                    elif attr == 'dv':
                        item.dv = int(random.choice(value.split(':')))
                    elif attr == 'av':
                        item.av = int(random.choice(value.split(':')))
                    elif attr == 'damage':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        min, max = pos[n].split(',')
                        item.min_damage = int(min)
                        item.max_damage = int(max)
                    elif attr == 'name':
                        item.name = value
                    elif attr == 'flags':
                        flags = value.split(',')
                        for flag in flags:
                            item.flags |= globals()[flag]
                    elif attr == 'fx':
                        fx, ch = value.split(',')
                        item.fx.append((globals()[fx], ch))
                    elif attr == 'pre' or attr == 'suf':
                        if d(100) < magic:
                            item.special = True
                            p = random.choice(value.split(':'))
                            globals()[p](item)
                    elif attr == 'amount':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        min, max = pos[n].split(',')
                        item.amount += random.randint(int(min),int(max))
                        item.name = str(item.amount) + ' ' + item.name
        return item
    
    @staticmethod
    def create_actor(name, stuff):
        actor = None
        
        sn = True
        br = False
        for index in xrange(0, len(stuff)):
            if not br:
                line = stuff[index]
                if line.strip() == '': continue
                if line[0] == '#':continue
                
                if sn:
                    if line[1:] == name:
                        actor = Actor(False)
                        sn = False
                        continue
                else:
                    
                    if line[0] == '*':
                        br = True
                        continue
                    
                    attr = line.split('=')[0]
                    value = line.split('=')[1]
                    
                    if attr == 'image':
                        actor.img_body = int(value), 0
                    elif attr == 'speed':
                        actor.speed = actor.cur_speed = int(value)
                    elif attr == 'ai':
                        ai_class = globals()[value]
                        actor.ai = ai_class(actor)
                    elif attr == 'name':
                        actor.name = value
                    elif attr == 'natural_av':
                        actor.natural_av = int(value)
        return actor
    
    @staticmethod
    def findAll(stuff):
        actors = []
        for line in stuff:
            if line.strip() == '': continue
            if line[0] == '*':
                actors.append(line[1:])
        return actors
