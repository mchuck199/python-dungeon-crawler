import random
from pdcglobal import *

def Endurance(actor):
    actor.cur_endurance += d(10) + d(10)

def Mind(actor):
    actor.cur_mind += d(10) + d(10)
    
def Spellcaster(actor):
    actor.cur_endurance += d(10) + d(10)
    actor.cur_mind += d(10) + d(10)

def Healing(actor):
    actor.cur_health += d(10)