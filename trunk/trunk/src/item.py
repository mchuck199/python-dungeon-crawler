from key_mapping import *
from pdcresource import *
from pdcglobal import *
import pygame

class Item(object):
    
    eq_tiles = None
    dd_tiles = None
    
    game = None
    
    def __init__(self, add):
        if add:
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
        self.equipped = False
        self.picked_up = False
        self.y = 0
        self.x = 0
        self.name = 'empty'
        self.flags = 0
        self.type = I_VOID
        
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    def pos(self):
        return self.x, self.y
    def clear_surfaces(self):
        self.eq_img_c = self.dd_img_c = None
        Item.dd_tiles = Item.eq_tiles = None

    def check_tiles(self):
        if Item.eq_tiles == None:
            Item.eq_tiles = Res('dc-pl.png', TILESIZE)
        
        if Item.dd_tiles == None:
            Item.dd_tiles = Res('dc-item.png', TILESIZE)
        
    def get_eq_img(self):
        self.check_tiles()
            
        if self.eq_img_c == None:
            if self.eq_img == None:
                self.eq_img_c = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
            else:
                self.eq_img_c = self.eq_tiles.get_subs(self.eq_img)
        return self.eq_img_c
    
    def get_dd_img(self):
        self.check_tiles()
            
        if self.dd_img_c == None:
            if self.dd_img == None:
                self.dd_img_c = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
            else:
                self.dd_img_c = self.dd_tiles.get(self.dd_img)
        return self.dd_img_c
