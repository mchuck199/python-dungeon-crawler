from actor import Humanoid   
from pdcglobal import d
from magic import *

class Human(Humanoid):
    desc = 'was versatile and talented at every topic.'
    def __init__(self, add, gender=0):
        Humanoid.__init__(self, add)
        self.img_body = 0 + gender, 0
        self.strength = self.cur_strength = 100 
        self.strength_heal = 1
        self.endurance = self.cur_endurance = 100
        self.endurance_heal = 2
        self.speed = self.cur_speed = 100
        self.speed_heal = 1
        self.mind = self.cur_mind = 100
        self.mind_heal = 2
        self.health = self.cur_health = 30
        self.health_heal = 1
        
class Alb(Humanoid):
    desc = 'was a quick and wiry person.'
    def __init__(self, add, gender=0):
        Humanoid.__init__(self, add)
        self.img_body = 10 + gender, 0
        self.strength = self.cur_strength = 100 - d(10)
        self.strength_heal = 1
        self.endurance = self.cur_endurance = 100 - d(10)
        self.endurance_heal = 3
        self.speed = self.cur_speed = 100 - d(10)
        self.speed_heal = 2
        self.mind = self.cur_mind = 100
        self.mind_heal = 1
        self.health = self.cur_health = 25
        self.health_heal = 1
        self.spells.append(LesserHaste())
        
class Naga(Humanoid):
    desc = 'was less talented in melee-weapons, but gifted in magic.'
    def __init__(self, add, gender=0):
        Humanoid.__init__(self, add)
        self.img_body = 16 + gender, 0
        self.strength = self.cur_strength = 100 - d(10) - d(10) 
        self.strength_heal = 1
        self.endurance = self.cur_endurance = 100 - d(10)
        self.endurance_heal = 1
        self.speed = self.cur_speed = 100 + d(10) + d(10)
        self.speed_heal = 1
        self.mind = self.cur_mind = 100 + d(10)
        self.mind_heal = 3
        self.health = self.cur_health = 30
        self.health_heal = 2
        spell = random.choice([FrostRay, HeatRay, LesserHealing, Regeneration, Identify])
        self.spells.append(spell())
        del self.slot.__dict__['trousers']
        del self.slot.slots['trousers']
        del self.slot.__dict__['boots']
        del self.slot.slots['boots']
        
races = (('Human', 0, 1, Human),
         ('Naga', 16, 17, Naga),
         ('Alb', 10, 11, Alb))

