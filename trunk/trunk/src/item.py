from key_mapping import *
from pdcresource import *
from pdcglobal import *
import pygame

class Item(object):
    
    eq_tiles = None
    dd_tiles = None
    
    game = None
    
    def __init__(self):
        self.game.items.append(self)
        self.cur_surf = None
        self.eq_img = None #pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        self.eq_img_c = None
        self.dd_img = None #pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        self.dd_img_c = None
        self.dv = 0
        self.av = 0
        self.min_damage = 1
        self.max_damage = 2

    def check_tiles(self):
        if Item.eq_tiles == None:
            Item.eq_tiles = Res('dc-pl.png', TILESIZE)
        
        if Item.dd_tiles == None:
            Item.dd_tiles = Res('dc-item.png', TILESIZE)

        
    def get_eq_img(self):
        self.check_tiles()
            
        if self.eq_img_c == None:
            if self.eq_img==None:
                self.eq_img_c = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
            else:
                self.eq_img_c = self.eq_tiles.get_subs(self.eq_img)
        return self.eq_img_c
    
    def get_dd_img(self):
        if Item.eq_tiles==None:
            Item.eq_tiles = Res('dc-pl.png', TILESIZE)
    
        if Item.dd_tiles==None:
            Item.dd_tiles = Res('dc-item.png', TILESIZE)
            
        if self.dd_img_c == None:
            if self.dd_img==None:
                self.dd_img_c = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
            else:
                self.dd_img_c = self.dd_tiles.get(self.dd_img)
        return self.dd_img_c
        
        
class Cloak(Item):
    def __init__(self):
        Item.__init__(self)
        self.eq_img = 45, 0
        self.dd_img = 159
        self.dv = 15

class Flail(Item):
    def __init__(self):
        Item.__init__(self)
        self.eq_img = 176, 1
        self.dd_img = 20
        self.av = 50
        self.min_damage = 2
        self.max_damage = 4
