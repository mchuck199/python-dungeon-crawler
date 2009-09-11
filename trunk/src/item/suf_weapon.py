import random
from effects import *

def SmallOfBattle(item):
    item.full_name += ' of Battle'
    item.av += 20

def SmallOfMaster(item):
    item.full_name += ' of the Master'
    item.av += random.randint(10, 30)

def SmallBull(item):
    item.full_name += ' of the Bull'
    item.av_fx.append((StunEffect, 30))

def SmallRedRain(item):
    item.full_name += ' of the Red Rain'
    item.av_fx.append((BleedEffect, random.randint(5, 20)))
    item.av += random.randint(20, 30)
