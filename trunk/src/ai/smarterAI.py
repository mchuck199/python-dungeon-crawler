from key_mapping import MOVE_WAIT
import pdcglobal as g
from actor import Actor
from ai import AI

class SmarterAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor)
        self.hostile.append(self.game.player.id)


    def stand_still(self):
        self.actor.move(MOVE_WAIT)

    def is_morale_down(self):
        return not self._morale()
    
    def is_morale_up(self):
        return self._morale()
        
    def _morale(self):
        hp = self.actor.cur_health
        max = self.actor.health
        return int(float(hp) / max * 100) > 100 - self.actor.morale

    def can_move_away_from_foe(self, foe):
        dir = self.actor.opposite_dir(foe)
        dirs = [dir]
        dirs.extend(self.build_alternate_dirs(dir,True))
        old_pos = self.actor.pos()
        for d in dirs:
            new_pos = g.get_new_pos(old_pos, d)
            result = self.game.is_move_valid(self.actor, new_pos)
            if result == True:
                return True
        return False
    
    def can_move_toward_foe(self, foe):
        x1, y1 = self.actor.pos()
        x2, y2 = foe.pos()
        if g.get_dis(x1, y1, x2, y2) <= 1:
            return False
        dir = self.actor.locateDirection(foe)
        dirs = [dir]
        dirs.extend(self.build_alternate_dirs(dir))
        old_pos = self.actor.pos()
        for d in dirs:
            new_pos = g.get_new_pos(old_pos, d)
            result = self.game.is_move_valid(self.actor, new_pos)
            if result == True:
                return True
        return False

    def to_close_to_foe(self, foe):
        if self.wanna_use_range():
            x1, y1 = self.actor.pos()
            x2, y2 = foe.pos()
            if g.get_dis(x1, y1, x2, y2) <= 4:
                return True
        else:
            return False
    
    def too_far_from_foe(self, foe):
        x1, y1 = self.actor.pos()
        x2, y2 = foe.pos()
        if self.wanna_use_range():
            if g.get_dis(x1, y1, x2, y2) > 7:
                return True
            return False
        if g.get_dis(x1, y1, x2, y2) > 1:
            return True
        return False    
 
    def move_away_from_foe(self, foe, dir=None):
        if dir != None:
            self.actor.move(dir)
            return
        dir = self.actor.opposite_dir(foe)
        dirs = [dir]
        dirs.extend(self.build_alternate_dirs(dir,True))
        old_pos = self.actor.pos()
        for d in dirs:
            new_pos = g.get_new_pos(old_pos, d)
            result = self.game.is_move_valid(self.actor, new_pos)
            if result == True:
                self.actor.move(d)
                return
        self.stand_still()
    
    def move_toward_foe(self, foe, dir=None):
        if dir != None:
            self.actor.move(dir)
            return
        dir = self.actor.locateDirection(foe)
        dirs = [dir]
        dirs.extend(self.build_alternate_dirs(dir))
        old_pos = self.actor.pos()
        for d in dirs:
            new_pos = g.get_new_pos(old_pos, d)
            result = self.game.is_move_valid(self.actor, new_pos)
            if result == True:
                self.actor.move(d)
                return
        self.stand_still()
    
    def can_attack_foe(self, foe):
        return True
    
    def wanna_use_range(self):
        if self.actor.ready_to_range():
            return True
        else:
            return False
    
    def attack_foe(self, foe):
        x1, y1 = self.actor.pos()
        x2, y2 = foe.pos()
        if self.wanna_use_range() and g.get_dis(x1, y1, x2, y2) > 1:
            if not self.actor.range_equipped():
                self.actor.equip_range()
                return
            else:
                self.actor.fire(foe.pos())
                return
        else:
            if not self.actor.melee_equipped():
                self.actor.equip_melee()
                return
            dir = self.actor.locateDirection(foe)
            self.actor.move(dir)
            return
        self.stand_still()
        print 'ouch'
    
    
    def act(self):
        
        if not self.seeing_player():
            self.stand_still()
            return
        
        foe = self.game.player
        
        if (self.is_morale_down() or self.to_close_to_foe(foe)) and self.can_move_away_from_foe(foe):
            self.move_away_from_foe(foe)
        elif (self.is_morale_up() and self.too_far_from_foe(foe)) and self.can_move_toward_foe(foe):
            self.move_toward_foe(foe)
        elif self.can_attack_foe(foe):
            self.attack_foe(foe)
        else:
             self.stand_still()
        
    
