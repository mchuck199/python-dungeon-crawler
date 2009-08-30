import pygame,os,random

TILESIZE = 32

MES_SYS = True

#colors
WHITE=255,255,255
GREEN=0,255,0
#maptiles
MT_INDEX = 0
MT_IMAGE = 1
MT_FLAGS = 2

QUIT = 1
SAVE = 2

#move modes
MM_WALK = 1
MM_FLY = 2
MM_SWIM = 4

#map-tile flags
F_WALKABLE = 1
F_FLYABLE = 2
F_SWIMABLE = 4
F_BLOCKSIGHT = 8
F_WALK_D = 16
F_FLY_D = 32
F_SWIN_D = 64
F_SC_UP = 128
F_SC_DOWN = 256
F_DIGABLE = 512
F_LIT = 1024
F_SML_LIT = 2048
F_MEMO = 4096

MAP_TILE_void = -1, 0, 0
MAP_TILE_floor = 0, 30, F_WALKABLE | F_FLYABLE
MAP_TILE_wall = 1, 9 , F_BLOCKSIGHT | F_DIGABLE
MAP_TILE_door = 2, 32, F_WALKABLE | F_FLYABLE
  
MAP_TILE_LIST = [MAP_TILE_void, MAP_TILE_floor, MAP_TILE_wall, MAP_TILE_door]

def d(side):
    return random.randint(1,side)

def line(x,y,x2,y2):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    if (x2 - x) > 0: sx = 1
    else: sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0: sy = 1
    else: sy = -1
    if dy > dx:
        steep = 1
        x,y = y,x
        dx,dy = dy,dx
        sx,sy = sy,sx
    d = (2 * dy) - dx
    for i in range(0,dx):
        if steep: coords.append((y,x))
        else: coords.append((x,y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    coords.append((x2,y2))
    return coords

def load_image(name):
        try:
            image = pygame.image.load(os.path.join('gfx', name))
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message

        image = image.convert_alpha()
        image.set_alpha(255, pygame.RLEACCEL)
        
        return image

class Debug():
    
    game_instance = None
    
    @staticmethod
    def init_debug(game):
        Debug.game_instance = game
        
    @staticmethod
    def debug(text):
        if MES_SYS:
            if Debug.game_instance != None:
                Debug.game_instance.message_queue.insert(0, '[DEBUG-MESSGAE:] ' + text)
            print text
