from pdcglobal import *

class GFX(object):
    game = None
    def __init__(self):
        self.redraw=True
    def get_surf(self):
        pass
    def pos(self):
        pass
    def tick(self):
        pass
    
class RayFX(GFX):
    def __init__(self, color1, color2, s_pos, t_pos):
        self.f_image = []
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color1, (15, 10), 2,2)
        pygame.draw.circle(surf, color2, (10, 15), 2,2)
        pygame.draw.circle(surf, color1, (20, 15), 2,2)
        self.f_image.append(surf)
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color2, (15, 10),2,2)
        pygame.draw.circle(surf, color1, (10, 15), 2,2)
        pygame.draw.circle(surf, color1, (20, 15), 2,2)
        self.f_image.append(surf)
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color1, (15, 10), 2,2)
        pygame.draw.circle(surf, color1, (10, 15), 2,2)
        pygame.draw.circle(surf, color2, (20, 15), 2,2)
        self.f_image.append(surf)
            
        self.c = 0
        self.image = self.f_image[self.c]
        self.__pos_gen = self.__pos(s_pos, t_pos)
        self.redraw=False
    def __pos(self, s_pos, t_pos):
        s_real = s_pos[0] * TILESIZE - self.game.camera.x * TILESIZE, s_pos[1] * TILESIZE - self.game.camera.y * TILESIZE
        t_real = t_pos[0] * TILESIZE - self.game.camera.x * TILESIZE, t_pos[1] * TILESIZE - self.game.camera.y * TILESIZE
        all = line(s_real[0], s_real[1], t_real[0], t_real[1])[::6]
        for pos in all:
            yield pos

    def get_surf(self):
        return self.image
    
    def pos(self):
        try:
            pos = self.__pos_gen.next()
            return pos
        except:
            return None
    
    def tick(self):
        #self.c += 1
        #if self.c >= len(RayFX.f_image): 
        #    self.c = 0
        self.c = random.randint(0, len(self.f_image) - 1)    
        self.image = self.f_image[self.c]

