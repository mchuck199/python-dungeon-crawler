from key_mapping import *
from pdcresource import *
from pdcglobal import *
from item import *
import pygame

class Actor(object):
    
    tiles = None
    game = None
    
    def __init__(self, add):
        Debug.debug('Creating Actor')
        if add: self.game.actors.append(self)
        self.name = 'Generic Actor'
        self.cur_surf = None
        self.img_body = None
        self.cloak = Item()
        self.armor = Item()
        self.boots = Item()
        self.right = Item()
        self.left = Item()
        self.head = Item()

        self.natural_dv = 10
        self.natural_av = 0
                
        self.x = 1
        self.y = 1
        
        self.move_mode = MM_WALK 
        
        self.timer = 0
        self.ai = None
        
        self.xp = 0
        self.strength = 100
        self.cur_strength = 100
        self.endurance = 100
        self.cur_endurance = 100
        self.speed = 100
        self.cur_speed = 100
        self.mind = 100
        self.cur_mind = 100
        self.health = 30
        self.cur_health = 30

        self.check_tiles()

    def check_tiles(self):
        if Actor.tiles == None:
            Actor.tiles = Res('dc-mon.png', TILESIZE)
    
    def die(self):
        self.game.actors.remove(self)
        
    def get_std_av(self):
        return self.cloak.av + self.armor.av + self.boots.av + self.right.av + self.left.av + self.head.av + self.natural_av
    def get_total_av(self):
        return self.cur_strength + self.cur_endurance / 2 + self.cur_mind / 4 + self.get_std_av() 
    
    def get_std_dv(self):
        return self.cloak.dv + self.armor.dv + self.boots.dv + self.right.dv + self.left.dv + self.head.dv + self.natural_dv
    def get_total_dv(self):
        return self.get_std_dv() + self.cur_endurance / 2 + self.cur_mind / 4
    
    def get_total_min_damage(self):
        return self.left.min_damage + self.cur_strength / 75
    def get_total_max_damage(self):
        return self.left.max_damage + self.cur_strength / 75

    def get_tile(self):
         
        self.check_tiles()
        
        surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)        
        
        surf.blit(self.cloak.get_eq_img(), (0, 0))
        surf.blit(self.tiles.get_subs(self.img_body), (0, 0))

        surf.blit(self.armor.get_eq_img(), (TILESIZE / 4, 0))
        surf.blit(self.boots.get_eq_img(), (0, TILESIZE / 2))
        
        surf.blit(self.right.get_eq_img(), (TILESIZE / 2, 0))
        surf.blit(self.left.get_eq_img(), (0, 0))
        surf.blit(self.head.get_eq_img(), (TILESIZE / 4, 0))
        
        return surf

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def tick(self):
        if self.cur_endurance < self.endurance:
            self.cur_endurance += 1
            
    def act(self):
        if self.ai != None:
            self.ai.act()

    def locateDirection(self, target):    
        """Checks in what direction the target is"""
        
        if self.x > target.x:
            if self.y == target.y:
                move_d = MOVE_LEFT
            elif self.y > target.y:
                move_d = MOVE_UP_LEFT
            else:
                move_d = MOVE_DOWN_LEFT
        
        if self.x < target.x:
            if self.y == target.y:
                move_d = MOVE_RIGHT
            elif self.y > target.y:
                move_d = MOVE_UP_RIGHT
            else:
                move_d = MOVE_DOWN_RIGHT
                
        if self.x == target.x:
            if self.y > target.y:
                move_d = MOVE_UP
            else:
                move_d = MOVE_DOWN
        
        return move_d

    def move(self, direction):
        pos = self.x, self.y
        new_pos = pos        
        if direction == MOVE_DOWN or direction == MOVE_DOWN_LEFT or direction == MOVE_DOWN_RIGHT:
            new_pos = new_pos[0], new_pos[1] + 1
        if direction == MOVE_UP or direction == MOVE_UP_LEFT or direction == MOVE_UP_RIGHT:
            new_pos = new_pos[0], new_pos[1] - 1
        if direction == MOVE_RIGHT or direction == MOVE_DOWN_RIGHT or direction == MOVE_UP_RIGHT:
            new_pos = new_pos[0] + 1, new_pos[1] 
        if direction == MOVE_LEFT or direction == MOVE_DOWN_LEFT or direction == MOVE_UP_LEFT:
            new_pos = new_pos[0] - 1, new_pos[1]
        
        result = Actor.game.is_move_valid(self, pos, new_pos, self.move_mode)     
        if isinstance(result, Actor):
            self.game.attack(self, result)
            self.timer += self.cur_speed
        elif result:
            self.x, self.y = new_pos[0], new_pos[1]
            self.timer += self.cur_speed
            self.game.map.cur_surf = None
            return True
        
        return False

class Humanoid(Actor):
    
    tiles = None

    def __init__(self,add):
        Actor.__init__(self,add)
        self.check_tiles()
        self.img_body = 1, 0
        self.name = 'Player'

    def check_tiles(self):
        if Humanoid.tiles == None:
            Humanoid.tiles = Res('dc-pl.png', TILESIZE)

    def get_tile(self):
        self.check_tiles()
        return Actor.get_tile(self) 
