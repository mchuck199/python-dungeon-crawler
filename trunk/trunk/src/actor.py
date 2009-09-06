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
        self.cloak = Item(False)
        self.armor = Item(False)
        self.boots = Item(False)
        self.right = Item(False)
        self.left = Item(False)
        self.head = Item(False)

        self.natural_dv = 10
        self.natural_av = 0
                
        self.x = 1
        self.y = 1
        
        self.move_mode = MM_WALK 
        
        self.timer = 0
        self.ai = None
        
        self.gold = 0
        
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
        #self.inv_size=8
        self.items = []
        self.spells = []

        self.fx = []

#        self.skills = {'Combat (Melee)':1,
#                       'Combat (Range)':4,
#                       'Evading':2,
#                       'Trap-Finding':0,
#                       'Magic (Order)':4,
#                       'Magic (Chaos)':3,
#                       'Magic (Spirit)':2,
#                       'Magic (Matter)':3}

    def take_off(self, item):
        if item.type == I_ARMOR:
            self.armor = Item(False)
        if item.type == I_BOOTS:
            self.boots = Item(False)
        if item.type == I_CLOAK:
            self.cloak = Item(False)
        if item.type == I_HELMET:
            self.head = Item(False)
        if item.type == I_SHIELD:
            self.right = Item(False)
        if item.type == I_WEAPON:
            self.left = Item(False)
        self.cur_surf = None
        self.items.append(item)
        item.equipped = False
    
    def drop(self, item):
        self.items.remove(item)
        self.game.items.append(item)
        item.picked_up = False
    
    def cast(self, spell):
        if self.cur_endurance < spell.phys_cost: return False
        if self.mind < spell.mind_cost: return False
        self.cur_endurance -= spell.phys_cost
        self.cur_mind -= spell.mind_cost
        
        return spell.cast(self)
    
    def get_equipment(self):
        return [item for item in (self.cloak,
                                  self.armor,
                                  self.boots,
                                  self.right,
                                  self.left,
                                  self.head) if not item.type == I_VOID]
    
    def pick_up(self, item):
        #items = self.game.get_item_at(self.pos)
        self.timer += self.cur_speed
        if item.type == I_GOLD:
            self.gold += item.amount
        else:
            self.items.append(item)
        self.game.items.remove(item)
        item.picked_up = True
        Debug.debug('%s picked up %s' % (self.name, item.name))

    def equip(self, item):
        self.timer += self.cur_speed
        self.items.remove(item)
        item.equipped = True
        
        if item.type == I_ARMOR:
            old = self.armor
            self.armor = item
        if item.type == I_BOOTS:
            old = self.boots
            self.boots = item
        if item.type == I_CLOAK:
            old = self.cloak
            self.cloak = item
        if item.type == I_HELMET:
            old = self.head
            self.head = item
        if item.type == I_SHIELD:
            old = self.right
            self.right = item
        if item.type == I_WEAPON:
            old = self.left
            self.left = item
        
        if not old.type == I_VOID:
            old.equipped = False
            self.items.append(old)
        self.cur_surf = None
        Debug.debug('%s equipped %s' % (self.name, item.name))

    def clear_surfaces(self):
        self.cur_surf = None
        Actor.tiles = None
        self.cloak.clear_surfaces()
        self.armor.clear_surfaces()
        self.boots.clear_surfaces()
        self.right.clear_surfaces()
        self.left.clear_surfaces()
        self.head.clear_surfaces()

    def check_tiles(self):
        if Actor.tiles == None:
            Actor.tiles = Res('dc-mon.png', TILESIZE)
    
    def die(self):
        if self in self.game.actors:
            self.game.actors.remove(self)
        if d(20) < 13:
            self.__drop_corpse()
        
    def __drop_corpse(self):
        Corpse(self)
        
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

    def pos(self):
        return self.x, self.y
    

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def tick(self):
        
        for e in self.fx:
            e.tick()
        
        if self.cur_endurance < self.endurance:
            self.cur_endurance += 3
            if self.cur_endurance > self.endurance:
                self.cur_endurance = self.endurance
        if self.cur_endurance > self.endurance:
            self.cur_endurance -= 1
        
        if self.cur_mind < self.mind:
            self.cur_mind += 1
        if self.cur_mind > self.mind:
            self.cur_mind -= 1
        
        if self.cur_health > self.health:
            self.cur_health -= 1
        
        if self.cur_speed > self.speed:
            self.cur_speed -= 1 
        if self.cur_speed < self.speed:
            self.cur_speed += 1
            
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
            if result != self:
                self.game.attack(self, result)
                self.timer += self.cur_speed
                return result
            else:
                self.timer += self.cur_speed
                return True
        elif result:
            self.x, self.y = new_pos[0], new_pos[1]
            self.timer += self.cur_speed
            [item.set_pos(self.pos()) for item in (self.cloak,
                                                   self.armor,
                                                   self.boots,
                                                   self.right,
                                                   self.left,
                                                   self.head)]
            [item.set_pos(self.pos()) for item in self.items]
            return True
        
        return False

class Humanoid(Actor):
    
    tiles = None

    def __init__(self, add):
        Actor.__init__(self, add)
        self.check_tiles()
        self.img_body = 1, 0
        self.name = 'Player'

    def check_tiles(self):
        if Humanoid.tiles == None:
            Humanoid.tiles = Res('dc-pl.png', TILESIZE)

    def get_tile(self):
        self.check_tiles()
        return Actor.get_tile(self) 
