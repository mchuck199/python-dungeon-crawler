import random
from pdcglobal import *

def PotionOfEndurance(item):
    item.full_name += ' of Endurance'
def DrinkPotionOfEndurance(self, actor):
    actor.cur_endurance += d(10) + d(10)
    
    
def PotionOfMind(item):
    item.full_name += ' of Mind'
def DrinkPotionOfMind(self, actor):
    actor.cur_mind += d(10) + d(10)
        
        
def PotionOfSpellcaster(item):
    item.full_name += ' of Spellcasters'
def DrinkPotionOfSpellcaster(self, actor):
    actor.cur_endurance += d(10) + d(10)
    actor.cur_mind += d(10) + d(10)


def PotionOfHealing(item):
    item.full_name += ' of Healing'
def DrinkPotionOfHealing(self, actor):
    actor.cur_health += d(10)
