import pygame, os, random

TILESIZE = 32

MES_SYS = False

#colors
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLACK = 0, 0, 0
BLUE = 80, 80, 255

#maptiles
MT_INDEX = 0
MT_IMAGE = 1
MT_FLAGS = 2

#item_types
I_VOID = 0
I_WEAPON = 1
I_SHIELD = 2
I_CLOAK = 4
I_ARMOR = 8
I_BOOTS = 16
I_HELMET = 32
I_STUFF = 64
I_GOLD=128

#game_states
S_RUN = 1
S_PLAYER_PICK_UP = 2
S_PLAYER_EQUIP = 3
S_PLAYER_CAST = 4
S_PLAYER_DROP = 5
S_PLAYER_TAKE_OFF = 6

CHOOSE_STATES = {S_PLAYER_PICK_UP:'Choose an item to pick up:',
                 S_PLAYER_EQUIP:'Choose an item to equip:',
                 S_PLAYER_CAST:'Choose a spell to cast:',
                 S_PLAYER_TAKE_OFF:'Choose an item to take off:',
                 S_PLAYER_DROP:'Choose an item to drop:'}

STATE_WORKER = {S_PLAYER_PICK_UP:'pickup',
                 S_PLAYER_EQUIP:'equip',
                 S_PLAYER_CAST:'cast',
                 S_PLAYER_TAKE_OFF:'take_off',
                 S_PLAYER_DROP:'drop'}

#quit messages
QUIT = 1
SAVE = 2

#move modes
MM_WALK = 1
MM_FLY = 2
MM_SWIM = 4

#item-flags
IF_EQUIPABLE = 1
IF_QUAFFABLE = 2
IF_EATABLE = 4

#map-tile flags
F_WALKABLE = 1
F_FLYABLE = 2
#F_SWIMABLE = 4
F_BLOCKSIGHT = 8
#F_WALK_D = 16
#F_FLY_D = 32
#F_SWIN_D = 64
F_SC_UP = 128
F_SC_DOWN = 256
F_DIGABLE = 512
#F_LIT = 1024
#F_SML_LIT = 2048
F_MEMO = 4096

MAP_TILE_void = 9, 0, 0
MAP_TILE_floor = 0, 1, F_WALKABLE | F_FLYABLE
MAP_TILE_wall = 1, 8 , F_BLOCKSIGHT | F_DIGABLE
MAP_TILE_door = 2, 32, F_WALKABLE | F_FLYABLE
MAP_TILE_down = 3, 42 , F_WALKABLE | F_SC_DOWN | F_FLYABLE
MAP_TILE_up = 4, 43 , F_WALKABLE | F_SC_UP | F_FLYABLE
  
MAP_TILE_LIST = [MAP_TILE_void, MAP_TILE_floor, MAP_TILE_wall,
                 MAP_TILE_door, MAP_TILE_down, MAP_TILE_up]

def d(side):
    return random.randint(1, side)

def line(x, y, x2, y2):
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
        x, y = y, x
        dx, dy = dy, dx
        sx, sy = sy, sx
    d = (2 * dy) - dx
    for i in range(0, dx):
        if steep: coords.append((y, x))
        else: coords.append((x, y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    coords.append((x2, y2))
    return coords

def sort_by_time(a, b):
    return a.timer - b.timer

def get_chars():
        c = 'abcdefghijklmonpqrstuvwxyz0123456789'
        for i in xrange(0, 27):
            yield c[i]

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
            #print text
