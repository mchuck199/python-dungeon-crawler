import random
from effects import *

def SmallOfBattle(item):
    item.name+=' of Battle'
    item.av+=20

def SmallOfMaster(item):
    item.name+=' of the Master'
    item.av+=random.randint(10,30)

def SmallBull(item):
    item.name+=' of the Bull'
    item.fx.append((StunEffect,30))

def SmallRedRain(item):
    item.name+=' of the Red Rain'
    item.fx.append((BleedEffect,random.randint(5,20)))
    item.av+=random.randint(20,30)