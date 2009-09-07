import pygame
import random
import os
import sys
import magic
import dungeon
 
from pygame import *
from ai import AI
from pdcglobal import *
from key_mapping import *
from shadowcast import sc
from camera import Camera
from item import Item
from cursor import Cursor
from actor import Actor, Humanoid
from populator import Populator
from eng_player_actions import *
from eng_state_worker import *
         
class Engine(object):
    def __init__(self):
        self.__message_queue = []
        self.__cur_stat_surf = None
        
        self.actors = []
        self.items = []
        self.quit_loop = False
        self.quit_mes = QUIT
        self.time = 0
        self.fow_surf = None
        self.stat_base_surf = load_image('stat.png')
        self.s48 = load_image('48.png')
        self.player_actions = PlayerActions(self)
        self.state_worker = StateWorker(self)
        self.camera = Camera(20, 26)
        self.state = S_RUN
        self.wait_for_target = None
        
        Debug.init_debug(self)
        Debug.debug('init pygame')

        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        
        self.__load_fonts()
        self.__set_game_instance()

        self.cursor = Cursor(self)
                
        self.player = Humanoid(True)
        i = dungeon.Populator.create_item('Flail', 'basic_weapons', 2)
        self.player.items.append(i)
        self.player.equip(i)
        #self.player.spells.append(magic.LesserHealing())
        #self.player.spells.append(magic.MajorHealing())
        #self.player.spells.append(magic.LesserHaste())
        #self.player.spells.append(magic.Identify())
        #self.player.spells.append(magic.FrostRay())
        #self.player.spells.append(magic.FoulnessRay())
        
        self._items_to_choose = {}
        self.random_map()

    def get_actor_at(self, pos):
        for actor in self.actors:
            if actor.pos() == pos:
                return actor
        return None

    def get_all_srd_actors(self, pos):
        new_pos = None
        mo = [(-1, -1), (-1, 0), (-1, 1),
              (1, -1), (1, 0), (1, 1),
              (0, -1), (0, 1)]
        
        poss=[]
        for m in mo:
            poss.append((m[0]+pos[0],m[1]+pos[1]))
        
        actors=[]
        for act in self.actors:
            if act.pos() in poss:
                actors.append(act)
        return actors

    def get_free_adj(self, pos):
        new_pos = None
        mo = [(-1, -1), (-1, 0), (-1, 1),
              (1, -1), (1, 0), (1, 1),
              (0, -1), (0, 1)]

        random.shuffle(mo) 
        while new_pos == None and len(mo) > 0: 
            t = mo.pop()
            new_pos = pos[0] + t[0], pos[1] + t[1]
            
            if not self.map.map_array[new_pos[1]][new_pos[0]][MT_FLAGS] & F_WALKABLE:
                new_pos = None
            else:
                for actor in self.actors:
                    if actor.pos() == new_pos:
                        new_pos = None
                        break
        
        return new_pos
        
    def get_sc_up_pos(self):
        y = 0
        x = 0
        for line in self.map.map_array:
            x = 0
            for t in line:
                if t == MAP_TILE_up:
                    pos = x, y
                x += 1
            y += 1
        return pos
    def get_sc_down_pos(self):
        y = 0
        x = 0
        for line in self.map.map_array:
            x = 0
            for t in line:
                if t == MAP_TILE_down:
                    pos = x, y
                x += 1
            y += 1
        return pos
    def shout(self, text):
        self.__message_queue.insert(0, text)    
    def random_map(self):
        self.actors = []
        self.actors.append(self.player)
        self.items = []
        self.map = dungeon.Map.Random()
        
        dungeon.Populator.fill_map_with_items(self.map, 'basic_weapons', 0, 5, 10)
        dungeon.Populator.fill_map_with_items(self.map, 'basic_stuff', 0, 5, 10)
        dungeon.Populator.fill_map_with_items(self.map, 'basic_books', 0, 5, 99)
        dungeon.Populator.fill_map_with_items(self.map, 'basic_potions', 0, 5, 99)
        dungeon.Populator.fill_map_with_creatures(self.map, 'easy_swarms', 0, 5)
        dungeon.Populator.fill_map_with_creatures(self.map, 'easy_other', 0, 5)
        dungeon.Populator.fill_map_with_creatures(self.map, 'easy_jelly', 0, 5)
        dungeon.Populator.fill_map_with_creatures(self.map, 'easy_golems', 0, 5)
                
        self.sc = sc(self.map.map_array)
        pos = self.get_sc_up_pos()
        self.player.set_pos(pos)
        r = self.camera.adjust(self.player.pos())
        while r:
            r = self.camera.adjust(self.player.pos())
            
    def start(self):
        Debug.debug('starting mainloop')
        return self._main_loop()
    def is_move_valid(self, actor, old_pos, new_pos, move_mode):
        for act in self.actors:
            if actor != act and act.pos() == new_pos:
                return act
            
        valid = self.map.is_move_valid(old_pos, new_pos, move_mode)
        if valid:
            if actor == self.player: 
                self.map.cur_surf = None    
                items = self.get_items_at(new_pos)
                if len(items) == 1:
                    self.shout('you see a %s' % (items[0].get_name()))
                if len(items) > 1:
                     self.shout('you see several items here')
        return valid
    def attack(self, attacker, victim):
        defence = victim.get_total_dv()
        attack = attacker.get_total_av()
        attack += d(100) + d(50)
        defence += 100 + d(100)
        Debug.debug('%s Attack: %i' % (attacker.name, attack))
        Debug.debug('%s Defense: %i' % (victim.name, defence))
        
        if victim == self.player:
            vi_adress = 'you'
        else:
            vi_adress = 'the ' + victim.name
        
        if attack >= defence:
            for fx in attacker.get_av_fx():
                if d(100) <= fx[1]:
                    Debug.debug('Applied effect %s to %s by %s' % (fx[0], victim, attacker))
                    f = fx[0](victim, attacker)
                    f.tick()
            
            for fx in victim.get_dv_fx():
                if d(100) <= fx[1]:
                    Debug.debug('Applied effect %s to %s by %s' % (fx[0], attacker, victim))
                    f = fx[0](attacker, victim)
                    f.tick()
            
            damage = random.randint(attacker.get_total_min_damage(), attacker.get_total_max_damage())
            Debug.debug('Hit for %i damage!' % (damage))
            killed = self.do_damage(victim, damage)
            if attacker == self.player:
                at_adress = 'You hit'
            else:
                at_adress = 'The ' + attacker.name + ' hits'
            self.shout('%s %s for %i damage.' % (at_adress, vi_adress, damage))
            if killed:
                if attacker == self.player:
                    at_adress = 'You killed'
                else:
                    at_adress = 'The ' + attacker.name + ' killed'
                self.shout('%s %s' % (at_adress, vi_adress))
        else:
            if attacker == self.player:
                at_adress = 'You miss'
            else:
                at_adress = attacker.name + ' misses'
            
            self.shout('%s %s.' % (at_adress, vi_adress))
            Debug.debug('Miss!')
            
        attacker.cur_endurance -= 1
        victim.cur_endurance -= 1
    def do_damage(self, act, dam, type=D_GENERIC):
        return act.do_damage(dam, type)
        
    def get_items_at(self, pos):
        return [item for item in self.items if item.pos() == pos]
    def redraw_map(self):
        self.map.cur_surf = None
    def redraw_stats(self):
        self.__cur_stat_surf = None
    def _game_over(self):
        print 'You failed'
        self.quit_loop = True
        sys.exit()
    def _save_quit(self):
        self.clock = None
        self.fow_surf = None
        self.__cur_stat_surf = None
        self.stat_base_surf = None
        self.s48 = None
        for act in self.actors: act.clear_surfaces()
        for item in self.items: item.clear_surfaces()

        self.quit_loop = True
        self.quit_mes = SAVE
    def _main_loop(self):
        while not self.quit_loop:
            self.clock.tick(60)
            self._world_move()
            self._world_draw()
            self._world_input()
#            print self.clock.get_fps()
        self.std_font = None
        return self.quit_mes
    def _world_input(self):
        for e in pygame.event.get():
            self.quit_loop = e.type == pygame.QUIT 
            
            if e.type == pygame.KEYDOWN:
                
                if e.key == GAME_SAVE_QUIT:
                    self._save_quit()
                
                # --- cheat keys >>>
                if e.key == pygame.K_F1:
                    for line in self.map.map_array:
                        l = ''
                        for s in line:
                            l = l + str(s[0])
                        print l    
                
                if e.key == pygame.K_F2:
                    self.player.cur_health = 200
                    self.player.cur_endurance = 5000
                    self.player.cur_mind = 5000
                    self.player.cur_strength = 5000
                    
                if e.key == pygame.K_F3:
                    for item in self.items:
                        print item.name, item.pos()

                if e.key == pygame.K_F4:                        
                    for act in self.actors:
                        print act.name, act.timer
                                    
                # <<< cheat keys ---
                
                self.__cur_stat_surf = None
                self.moved = True
                
                if self.state == S_RUN:
                    if e.key in PLAYER_ACTIONS: 
                        self.player_actions.__getattribute__(PLAYER_ACTIONS[e.key])()

                elif self.state in STATE_WORKER:
                    self.state_worker.__getattribute__(STATE_WORKER[self.state])(e.key)

        if self.state == S_PLAYER_CURSOR:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            [self.cursor.move(key) for key in MOVES if keys[key]]

        if self.state == S_RUN:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            [self.player.move(key) for key in MOVES if keys[key] and self.player.timer <= 0]
    def _world_move(self):
        if self.state == S_RUN:
            self.sc.do_fov(self.player.x, self.player.y, self.player.cur_mind / 20 + 5)
            self.actors.sort(sort_by_time) #actors with lowest timer first
            diff = self.actors[0].timer
            self.time += diff
            
            if self.time > 1500:             #act-independent issues
                [act.tick() for act in self.actors]
                self.time -= 1500
                    
            for actor in self.actors:
                if actor.timer > 0:
                    actor.timer -= diff
                else:
                    actor.act()
    def _world_draw(self):
        if self.camera.adjust(self.player.pos()):
            self.map.cur_surf = None
        self.screen.fill((0, 0, 0))
        if not self.player.dazzled:
            self.screen.blit(self.__get_map_surface(), (-self.camera.x * TILESIZE, -self.camera.y * TILESIZE))
        
        if not self.player.dazzled:
            for item in self.items: 
                if not item.picked_up and (self.sc.lit(item.x, item.y) or self.player.x == item.x and self.player.y == item.y):
                    try:
                        self.screen.blit(self.__get_item_surface(item), (item.x * TILESIZE - self.camera.x * TILESIZE, item.y * TILESIZE - self.camera.y * TILESIZE))
                    except:
                        item.cur_surf = None
                        self.screen.blit(self.__get_item_surface(item), (item.x * TILESIZE - self.camera.x * TILESIZE, item.y * TILESIZE - self.camera.y * TILESIZE))
        
        for act in self.actors:
            if self.sc.lit(act.x, act.y) and not self.player.dazzled or act == self.player:
                self.screen.blit(self.__get_actor_surface(act), (act.x * TILESIZE - self.camera.x * TILESIZE, act.y * TILESIZE - self.camera.y * TILESIZE))
        
        if self.state == S_PLAYER_CURSOR:
            self.screen.blit(self.cursor.get_surf(), (self.cursor.x * TILESIZE - self.camera.x * TILESIZE, self.cursor.y * TILESIZE - self.camera.y * TILESIZE))
        
        self.screen.blit(self.__get_message_surface(), (0, 768 - 128))
        self.screen.blit(self.__get_statblock_surface(), (1024 - 192, 0))
        pygame.display.flip()

    def __get_map_surface(self):
        if self.map.cur_surf == None:
            surf_map = pygame.Surface((self.map.width * TILESIZE, self.map.height * TILESIZE))
            cx, cy, cw, ch = self.camera.get_view_port()       
            for x in xrange(max(cx, 0), min(self.map.width, cw + 1)):
            #for x in xrange(self.map.width):
                
                #for y in xrange(self.map.height):
                for y in xrange(max(cy, 0), min(self.map.height, ch + 1)):
                    #if self.camera.is_in_view(x, y):
                    pos = (x, y) == self.player.pos() 
                    lit = self.sc.lit(x, y)
                    memo = self.map.map_array[y][x][MT_FLAGS] & F_MEMO
                    if pos or lit or memo:
                        blit_position = (x * TILESIZE, y * TILESIZE)
                        surf_map.blit(self.map.get_tile_at(x, y), blit_position)
                        
                        if not pos and not lit and memo:
                            surf_map.blit(self.__get_fow(), blit_position)
                        
                        if not self.map.map_array[y][x][MT_FLAGS] & F_MEMO:
                            tile = self.map.map_array[y][x]
                            new_tile = tile[0], tile[1], tile[2] ^ F_MEMO
                            self.map.map_array[y][x] = new_tile

            self.map.cur_surf = surf_map
        
        return self.map.cur_surf
    def __get_actor_surface(self, act):
        if act.cur_surf == None:
            surf_act = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)
            surf_act.blit(act.get_tile(), (0, 0)) 
            act.cur_surf = surf_act
        return act.cur_surf
    def __get_item_surface(self, item):
        if item.cur_surf == None:
            surf_item = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)
            surf_item.blit(item.get_dd_img(), (0, 0)) 
            item.cur_surf = surf_item
        return item.cur_surf
    def __get_message_surface(self):
        surf = pygame.Surface((1024 - 192, 128))
        surf.fill((120, 120, 0))
        y = 100
        for mes in self.__message_queue:
            text = self.std_font.render(mes, True, WHITE)
            surf.blit(text, (0, y))
            y -= 20
        return surf
    def __get_statblock_surface(self):
        if self.__cur_stat_surf == None:
            surf = pygame.Surface((192, 768))
            surf.blit(self.stat_base_surf, (0, 0))
            
            if self.state == S_RUN:
                self.__draw_stat_block(surf)    

            if self.state in CHOOSE_STATES:
                self.__draw_item_choose(surf, CHOOSE_STATES[self.state])
            
            self.__cur_stat_surf = surf
            
        return self.__cur_stat_surf
    
    def __set_game_instance(self):
        dungeon.Map.game = self
        Actor.game = self
        Item.game = self
        AI.game = self
        Camera.game = self
        dungeon.Populator.game = self
        magic.Spell.game = self
    
    def __draw_item_choose(self, surf, message):
        self.__render_text(surf, message, WHITE, (16, 20))
        y = 38
        abc = self._items_to_choose.keys()
        abc.sort()
        for key in abc:
            item = self._items_to_choose[key]
            color = WHITE
            if hasattr(item, 'special'):
                if item.special:
                    color = GREEN
            elif hasattr(item, 'color'):
                color = item.color    
            if hasattr(item, 'get_name'):
                name = item.get_name()
            else:
                name = item.name
            
            self.__render_text(surf, '%s -' % (key), WHITE, (16, y))
            self.__render_text(surf, name, color, (32, y)); y += 18
            
            info = item.info()
            
            for line in item.info():
                self.__render_text(surf, line, color, (32, y)); y += 18
            
    def __draw_stat_block(self, surf):
        s48 = pygame.Surface.copy(self.s48)
        
        head = pygame.transform.smoothscale(self.player.slot.head.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 16))
        surf.blit(head, (192 / 2 - 24, 16))
                
        shield = pygame.transform.smoothscale(self.player.slot.shield.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 + 32, 72))
        surf.blit(shield, (192 / 2 + 32, 72))
                
        weapon = pygame.transform.smoothscale(self.player.slot.weapon.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 80, 72))
        surf.blit(weapon, (192 / 2 - 80, 72))
        
        armor = pygame.transform.smoothscale(self.player.slot.armor.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 126))
        surf.blit(armor, (192 / 2 - 24, 126))
        
        cloak = pygame.transform.smoothscale(self.player.slot.cloak.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 72))
        surf.blit(cloak, (192 / 2 - 24, 72))
        
        boots = pygame.transform.smoothscale(self.player.slot.boots.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 184))
        surf.blit(boots, (192 / 2 - 24, 184))
                
        stats = [self.std_font.render('Strength: ', True, WHITE), self.std_font.render('Endurance: ', True, WHITE), self.std_font.render('Mind: ', True, WHITE), self.std_font.render('Speed: ', True, WHITE), self.std_font.render('Health: ', True, WHITE)]
        y = 235
        for line in stats:
            surf.blit(line, (16, y))
            y += 18
        
        stats = [self.std_font.render(str(self.player.strength), True, WHITE), self.std_font.render(str(self.player.endurance), True, WHITE), self.std_font.render(str(self.player.mind), True, WHITE), self.std_font.render(str(self.player.speed), True, WHITE), self.std_font.render(str(self.player.health), True, WHITE)]
        y = 235
        for line in stats:
            surf.blit(line, (90, y))
            y += 18
        
        stats = [self.std_font.render(str(self.player.cur_strength), True, GREEN), self.std_font.render(str(self.player.cur_endurance), True, GREEN), self.std_font.render(str(self.player.cur_mind), True, GREEN), self.std_font.render(str(self.player.cur_speed), True, GREEN), self.std_font.render(str(self.player.cur_health), True, GREEN)]
        y = 235
        for line in stats:
            surf.blit(line, (120, y))
            y += 18
        
        stats = [self.std_font.render('Attack: ', True, WHITE), self.std_font.render('Defense: ', True, WHITE), self.std_font.render('Damage: ', True, WHITE)]
        y = 330
        for line in stats:
            surf.blit(line, (16, y))
            y += 20
        
        stats = [self.std_font.render(str(self.player.get_total_av()), True, WHITE), self.std_font.render(str(self.player.get_total_dv()), True, WHITE), self.std_font.render(str(self.player.get_total_min_damage()) + '-' + str(self.player.get_total_max_damage()), True, WHITE)]
        y = 330
        for line in stats:
            surf.blit(line, (90, y))
            y += 20

        
        gold = self.std_font.render('Gold:', True, WHITE)
        amount = self.std_font.render(str(self.player.gold), True, WHITE)
        surf.blit(gold, (16, 430))
        surf.blit(amount, (90, 430))
        
#        y = 430            
#        skills= self.player.skills
#        for skill in skills:
#            line = self.std_font.render(skill, True, WHITE)
#            surf.blit(line, (16, y))
#            y += 20
#        
#        y = 430    
#        for skill in skills:
#            pr=''
#            for _ in xrange(skills[skill]): pr+='*'
#            line = self.std_font.render(pr, True, WHITE)
#            surf.blit(line, (90, y))
#            y += 20
    def __get_fow(self):
        if self.fow_surf == None:
            self.fow_surf = pygame.Surface((TILESIZE, TILESIZE))
            self.fow_surf.fill(BLACK)
            self.fow_surf.set_alpha(100)
        return self.fow_surf
    def __render_text(self, surf, text, color, pos):
        t = self.std_font.render('%s' % (text), True, color)
        ts = self.std_font.render('%s' % (text), True, BLACK)
        surf.blit(ts, (pos[0] + 1, pos[1] + 1))
        surf.blit(t, pos)
    def __load_fonts(self):
        self.std_font = pygame.font.Font(os.path.join('font', 'jesaya.ttf'), 14)
    
    def re_init(self):
        Debug.debug('re_init')
        self.__load_fonts()
        self.quit_loop = False
        self.quit_mes = QUIT
        self.stat_base_surf = load_image('stat.png')
        self.s48 = load_image('48.png')
        if hasattr(self, 'map'):
            self.map.cur_surf = None
        self.clock = pygame.time.Clock()
        self.__set_game_instance()        
