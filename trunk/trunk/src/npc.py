from key_mapping import *
from pdcresource import *
from pdcglobal import *
from ai import *
from actor import Actor
import pygame

class Slug(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.img_body = 280, 0
        self.speed = 200
        self.cur_speed=200
        self.ai = ChasePlayerAI(self)
        self.name = 'Slug'
        self.natural_av = 30
        
class FloatingEye(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.img_body = 135, 0
        self.speed = 450
        self.ai = SimpleAI(self)
        self.name = 'Floating Eye'
        
        
        
