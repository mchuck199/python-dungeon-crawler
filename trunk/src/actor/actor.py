from key_mapping import *
from pdcresource import *
from pdcglobal import *
from item import *
from slot import *
import pygame

class Actor(object):
    
    tiles = None
    game = None
    
    def __init__(self, add):
        Debug.debug('Creating Actor')
        self.game.add_actor(self, add)
        self.name = 'Generic Actor'
        self.cur_surf = None
        self.img_body = None
        self.id = self.game.get_id()
        self.slot = Slot(self)
        
        self.natural_dv = 10
        self.natural_av = 0

        self.align_co = 0
        self.align_ge = 0
                
        self.x = 1
        self.y = 1
        
        self.morale = 75
        
        self.move_mode = MM_WALK 
        
        self.timer = 0
        self.ai = None
        
        self.gold = 0
        self.xp_value = 25
        self.xp = 0
        
        self.strength = 100
        self.cur_strength = 100
        self.strength_heal = 1
        
        self.endurance = 100
        self.cur_endurance = 100
        self.endurance_heal = 3
        
        self.speed = 100
        self.cur_speed = 100
        self.speed_heal = 1
        
        self.mind = 100
        self.cur_mind = 100
        self.mind_heal = 1
        
        self.health = 30
        self.cur_health = 30
        self.health_heal = 1

        self.check_tiles()
        #self.inv_size=8
        self.items = []
        self.spells = []

        self.av_fx = []
        self.dv_fx = []
        self.running_fx = []
        
        self.ch_drop_corpse = 33
        
        self.min_damage = 1
        self.max_damage = 3
        self.classkit = None
        self.dazzled = False

#       self.skills = {'Combat (Melee)':1,
#                       'Combat (Range)':4,
#                       'Evading':2,
#                       'Trap-Finding':0,
#                       'Magic (Order)':4,
#                       'Magic (Chaos)':3,
#                       'Magic (Spirit)':2,
#                       'Magic (Matter)':3}

    def gain_xp(self, amount):
        self.xp += amount

    def get_av_fx(self):
        fx = [f for f in self.av_fx]
        for item in self.get_equipment():
            for f in item.av_fx:
                fx.append(f)
        return fx

    def get_dv_fx(self):
        fx = [f for f in self.dv_fx]
        for item in self.get_equipment():
            for f in item.dv_fx:
                fx.append(f)
        return fx

    def redraw(self):
        self.cur_surf = None

    def clear_surfaces(self):
        for item in self.items:
            item.clear_surfaces()
        self.cur_surf = None
        Actor.tiles = None
        self.slot.clear_surfaces()

    def do_damage(self, dam, type):
        if self.game.player == self:
            self.game.redraw_stats()
        self.cur_health -= dam
        if self.cur_health < 1:
            self.die()
            if self.game.player == self:
                self.game.game_over()
            Debug.debug('%s dies of damage' % (self.name))
            return True
        return False

    def lose_endurance(self, amount, from_fight=False):
        if from_fight and self.cur_endurance < self.endurance / 2:
            if (50) < 100:
                return
        self.cur_endurance -= amount
        if self.cur_endurance < 1:
            self.cur_endurance = 0

    def read(self, item):
        self.timer += self.cur_speed
        item.read(item, self)

    def drink(self, item):
        self.items.remove(item)
        self.timer += self.cur_speed
        item.drink(item, self)
        
    def equip(self, item):
        if self.slot.equip(item): 
            self.timer += self.cur_speed
            self.redraw()
            Debug.debug('%s equipped %s' % (self.name, item.get_name()))
            return True
        return False

    def take_off(self, item):
        self.timer += self.cur_speed
        self.slot.take_off(item)
        self.redraw()
        Debug.debug('%s took off %s' % (self.name, item.get_name()))
    
    def drop(self, item):
        self.items.remove(item)
        self.game.add_item(item)
        item.picked_up = False
    def fire(self, pos):
        self.timer += self.cur_speed
        if not self.slot.ammo.used():
            self.slot.ammo = Item(False)
        self.game.range_attack(self, pos)
        
    def cast(self, spell):
        if self.cur_endurance < spell.phys_cost: return False
        if self.mind < spell.mind_cost: return False
        self.cur_endurance -= spell.phys_cost
        self.cur_mind -= spell.mind_cost
        self.timer += self.cur_speed
        return spell.cast(self)
    
    def get_equipment(self):
        return self.slot.get_equipment()
    
    def pick_up(self, item):
        self.timer += self.cur_speed
        if item.type == I_GOLD:
            self.gold += item.amount
        else:
            self.items.append(item)
        self.game.del_item(item)
        item.picked_up = True
        Debug.debug('%s picked up %s' % (self.name, item.get_name()))

    def check_tiles(self):
        if Actor.tiles == None:
            Actor.tiles = Res('dc-mon.png', TILESIZE)
    
    def die(self):
        self.game.del_actor(self)
        if d(100) < self.ch_drop_corpse:
            self.__drop_corpse()
        for item in self.slot.get_equipment():
            self.take_off(item)
            self.drop(item)
        for item in self.items:
            self.drop(item)
        if self.ai != None:
            self.ai.kill = True
    def __drop_corpse(self):
        Corpse(self)
        
    def get_std_av(self):
        items = self.slot.get_equipment()
        av = self.natural_av
        for item in items:
            av += item.av
        return av
    def get_total_av(self):
        av = self.cur_strength + self.cur_endurance / 2 + self.cur_mind / 4 + self.get_std_av()
        if self.dazzled:
            av /= 5
        return av
    
    def get_std_dv(self):
        items = self.slot.get_equipment()
        dv = self.natural_dv
        for item in items:
            dv += item.dv
        return dv
    def get_total_dv(self):
        dv = self.get_std_dv() + self.cur_endurance / 2 + self.cur_mind / 4
        if self.dazzled:
            dv /= 5
        return dv
    
    def equip_melee(self):
        melee_weapons = []
        if self.slot.weapon.flags & IF_MELEE:
            melee_weapons.append(self.slot.weapon)
        for item in self.items:
            if item.flags & IF_MELEE:
                melee_weapons.append(item)
        if len(melee_weapons) > 0:
            melee_weapons.sort(cmp=lambda x, y: x.av - y.av)
            self.equip(melee_weapons[0])
        
    def equip_range(self):
        range_weapons = []
        if self.slot.weapon.flags & IF_RANGED:
            range_weapons.append(self.slot.weapon)
            
        for item in self.items:
            if item.flags & IF_RANGED:
                range_weapons.append(item)
        
        ammos = []
        if self.slot.ammo.type != I_VOID:
            self.ammos.append(self.slot.ammo)
            
        for item in self.items:
            if item.__class__.__name__ == 'Ammo':
                ammos.append(item)

        for weapon in range_weapons:
            for ammo in ammos:
                    if ((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                        (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                        self.equip(weapon)
                        self.equip(ammo)
                        return

    def melee_equipped(self):
        weapon = self.slot.weapon
        if weapon.flags & IF_MELEE:
            return True
        return False
            
    def range_equipped(self):
        weapon = self.slot.weapon
        if weapon.flags & IF_RANGED:
            ammo = self.slot.ammo
            if ((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                return True
        return False
        
    def ready_to_range(self):
        range_weapons = []
        
        if self.slot.weapon.flags & IF_RANGED:
            range_weapons.append(self.slot.weapon)
            
        for item in self.items:
            if item.flags & IF_RANGED:
                range_weapons.append(item)
        
        ammos = []
        if self.slot.ammo.type != I_VOID:
            ammos.append(self.slot.ammo)
            
        for item in self.items:
            if item.__class__.__name__ == 'Ammo':
                ammos.append(item)

        for weapon in range_weapons:
            for ammo in ammos:
                    if ((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                        (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                        return True
        
        return False

    def get_total_min_damage(self, range=False):
        if self.slot.weapon.type != I_VOID:
            if range:
                weapon = self.slot.weapon
                if weapon.flags & IF_RANGED:
                    ammo = self.slot.ammo
                    if ((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                        (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                        return max(1, ammo.min_damage + (self.cur_strength - 100) / 18)
            
            return max(1, self.slot.weapon.min_damage + (self.cur_strength - 100) / 9)
        else:
            return max(1, self.min_damage + (self.cur_strength - 100) / 9)
    def get_total_max_damage(self, range=False):
        if self.slot.weapon.type != I_VOID:
            if range:
                weapon = self.slot.weapon
                if weapon.flags & IF_RANGED:
                    ammo = self.slot.ammo
                    if ((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                        (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                        return max(1, ammo.max_damage + (self.cur_strength - 100) / 18)

            return max(1, self.slot.weapon.max_damage + (self.cur_strength - 100) / 9)
        else:
            return max(1, self.max_damage + (self.cur_strength - 100) / 9)
    def get_tile(self):
         
        self.check_tiles()
        
        surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)        
        surf.blit(self.slot.cloak.get_eq_img(), (0, 0))
        surf.blit(self.tiles.get_subs(self.img_body), (0, 0))

        surf.blit(self.slot.armor.get_eq_img(), (TILESIZE / 4, 0))
        
        if hasattr(self.slot, 'trousers'):
            surf.blit(self.slot.trousers.get_eq_img(), (0, TILESIZE / 2))
        
        if hasattr(self.slot, 'boots'):
            surf.blit(self.slot.boots.get_eq_img(), (0, TILESIZE / 2))
        
        surf.blit(self.slot.shield.get_eq_img(), (TILESIZE / 2, 0))
        surf.blit(self.slot.weapon.get_eq_img(), (0, 0))
        surf.blit(self.slot.head.get_eq_img(), (TILESIZE / 4, 0))
        
        return surf

    def pos(self):
        return self.x, self.y
   
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def tick(self):
        
        self.dazzled = False
        
        for e in self.running_fx:
            e.tick()
        
        if self.cur_endurance < self.endurance:
            self.cur_endurance += self.endurance_heal
            if self.cur_endurance > self.endurance:
                self.cur_endurance = self.endurance
        
        if self.cur_endurance > self.endurance:
            self.cur_endurance -= 1
        
        if self.cur_mind < self.mind:
            self.cur_mind += self.mind_heal
            if self.cur_mind > self.mind:
                self.cur_mind = self.mind
                
        if self.cur_mind > self.mind:
            self.cur_mind -= 1
            
        
        if self.cur_health > self.health:
            self.cur_health -= 1
        
        if self.cur_health < self.health:
            self.cur_health += self.health_heal
            if self.cur_health > self.health:
                self.cur_health = self.health
                
        if self.cur_speed < self.speed:
            self.cur_speed += 1 
        
        if self.cur_speed > self.speed:
            self.cur_speed -= self.speed_heal
            if self.cur_speed < self.speed:
                self.cur_speed = self.speed
            
        if self.cur_strength > self.strength:
            self.cur_strength -= 1 
        if self.cur_strength < self.strength:
            self.cur_strength += self.strength_heal
            if self.cur_strength > self.strength:
                self.cur_strength = self.strength
            
    def act(self):
        if self.ai != None:
            self.ai.act()

    def opposite_dir(self, target):
        if hasattr(target, 'x'):
            tx = target.x
            ty = target.y
        else:
            tx = target[0]
            ty = target[1]
        
        if self.x > tx:
            if self.y == ty:
                move_d = MOVE_RIGHT
            elif self.y > ty:
                move_d = MOVE_DOWN_RIGHT
            else:
                move_d = MOVE_UP_RIGHT
        
        if self.x < tx:
            if self.y == ty:
                move_d = MOVE_LEFT
            elif self.y > ty:
                move_d = MOVE_DOWN_LEFT
            else:
                move_d = MOVE_UP_LEFT
                
        if self.x == tx:
            if self.y > ty:
                move_d = MOVE_DOWN
            else:
                move_d = MOVE_UP
        
        return move_d

    def locateDirection(self, target):    
        """Checks in what direction the target is"""

        if hasattr(target, 'x'):
            tx = target.x
            ty = target.y
        else:
            tx = target[0]
            ty = target[1]
        
        if self.x > tx:
            if self.y == ty:
                move_d = MOVE_LEFT
            elif self.y > ty:
                move_d = MOVE_UP_LEFT
            else:
                move_d = MOVE_DOWN_LEFT
        
        if self.x < tx:
            if self.y == ty:
                move_d = MOVE_RIGHT
            elif self.y > ty:
                move_d = MOVE_UP_RIGHT
            else:
                move_d = MOVE_DOWN_RIGHT
                
        if self.x == tx:
            if self.y > ty:
                move_d = MOVE_UP
            else:
                move_d = MOVE_DOWN
        
        return move_d

    def move(self, direction):
        if direction == MOVE_WAIT:
            self.timer += self.cur_speed
            return True
        
        new_pos = get_new_pos(self.pos(), direction)
        
        result = self.game.is_move_valid(self, self.pos(), new_pos, self.move_mode)
             
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
            [item.set_pos(self.pos()) for item in self.slot.get_equipment()]
            [item.set_pos(self.pos()) for item in self.items]
            return True
        
        return False

class Humanoid(Actor):
    
    tiles = None

    def __init__(self, add):
        Actor.__init__(self, add)
        self.t = None
        self.check_tiles()
        self.img_body = 1, 0
        self.name = 'Player'

    def check_tiles(self):
        if Humanoid.tiles == None:
            Humanoid.tiles = Res('dc-pl.png', TILESIZE)
        
    def get_tile(self):
        self.check_tiles()
        return Actor.get_tile(self)
    
    def clear_surfaces(self):
        Actor.clear_surfaces(self)
        for item in self.items:
            item.clear_surfaces()
        self.cur_surf = None
        Humanoid.tiles = None
        self.slot.clear_surfaces()
