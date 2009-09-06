from pdcglobal import *
import pygame

class StateWorker(object):
    def __init__(self, game):
        self.game = game
        
    def take_off(self, key):
        if pygame.key.name(key) in self.game._items_to_choose.keys():
            item = self.game._items_to_choose[pygame.key.name(key)]
            self.game.player.take_off(item)
            self.game.message_queue.insert(0, 'You took of %s' % (item.name))
            self.game.state = S_RUN
        elif key == pygame.K_ESCAPE:
            self.game.state = S_RUN
        
    def drop(self, key):
         if pygame.key.name(key) in self.game._items_to_choose.keys():
            item = self.game._items_to_choose[pygame.key.name(key)]
            self.game.player.drop(item)
            self.game.message_queue.insert(0, 'You dropped %s' % (item.name))
            self.game.state = S_RUN
         elif key == pygame.K_ESCAPE:
            self.game.state = S_RUN
            
    def pickup(self, key):
        if pygame.key.name(key) in self.game._items_to_choose.keys():
            item = self.game._items_to_choose[pygame.key.name(key)]
            self.game.player.pick_up(item)
            self.game.message_queue.insert(0, 'You picked up a %s' % (item.name))
            self.game.state = S_RUN
        elif key == pygame.K_ESCAPE:
            self.game.state = S_RUN
    def equip(self, key):
        if pygame.key.name(key) in self.game._items_to_choose.keys():
            item = self.game._items_to_choose[pygame.key.name(key)]
            self.game.player.equip(item)
            self.game.message_queue.insert(0, 'You equipped %s' % (item.name))
            self.game.state = S_RUN
        elif key == pygame.K_ESCAPE:
            self.game.state = S_RUN
    def cast(self, key):
        if pygame.key.name(key) in self.game._items_to_choose.keys():
            spell = self.game._items_to_choose[pygame.key.name(key)]
            if self.game.player.cur_endurance > spell.phys_cost:
                if self.game.player.cur_mind > spell.mind_cost:
                    self.game.player.cast(spell)
                    self.game.message_queue.insert(0, 'You cast %s' % (spell.name))
                else:
                    self.game.message_queue.insert(0, "You don't have enough mind to cast %s" % (spell.name))
            else:
                self.game.message_queue.insert(0, "You don't have enough endurance to cast %s" % (spell.name))
            self.game.state = S_RUN
        elif key == pygame.K_ESCAPE:
            self.game.state = S_RUN
