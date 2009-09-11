import pygame, os, random, math
from key_mapping import *

TILESIZE = 32

MES_SYS = False# True

#colors
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLACK = 0, 0, 0
BLUE = 80, 80, 255
RED = 255, 0, 0
PURPLE = 255, 0, 255
YELLOW = 255, 255, 0
#maptiles
MT_INDEX = 0
MT_IMAGE = 1
MT_FLAGS = 2

#map_types
DG_BSD = 0

#item_types
I_VOID = 0x0
I_WEAPON = 0x1
I_SHIELD = 0x2
I_CLOAK = 0x4
I_ARMOR = 0x8
I_BOOTS = 0x10
I_HELMET = 0x20
I_STUFF = 0x40
I_GOLD = 0x80
I_TROUSERS = 0x100
I_AMMO = 0x200


#spell-types
ST_GENERIC = 1
ST_CHAOS = 2
ST_ORDER = 4
ST_FIRE = 8
ST_COLD = 16

#damage_types
D_GENERIC = 0x1
D_FIRE = 0x2
D_COLD = 0x4
D_ACID = 0x8
D_CHAOS = 0x10
D_ORDER = 0x20
D_PIERCE = 0x40
D_BLUDGE = 0x80
D_SLASH = 0x100
D_POISON = 0x200
#game_states
S_RUN = 1
S_PLAYER_PICK_UP = 2
S_PLAYER_EQUIP = 3
S_PLAYER_CAST = 4
S_PLAYER_DROP = 5
S_PLAYER_TAKE_OFF = 6
S_PLAYER_DRINK = 7
S_PLAYER_READ = 8
S_PLAYER_IDENTIFY = 9
S_PLAYER_CURSOR = 10
S_GFX = 11
S_PLAYER_STATS = 12

CHOOSE_STATES = {S_PLAYER_PICK_UP:'Choose an item to pick up:',
                 S_PLAYER_EQUIP:'Choose an item to equip:',
                 S_PLAYER_CAST:'Choose a spell to cast:',
                 S_PLAYER_TAKE_OFF:'Choose an item to take off:',
                 S_PLAYER_DROP:'Choose an item to drop:',
                 S_PLAYER_DRINK:'Choose an item to drink:',
                 S_PLAYER_READ:'Choose an item to read',
                 S_PLAYER_IDENTIFY: 'Choose an item to identify',
                 S_PLAYER_STATS: 'Choose an attribute to improve:'}

STATE_WORKER = {S_PLAYER_PICK_UP:'pickup',
                 S_PLAYER_EQUIP:'equip',
                 S_PLAYER_CAST:'cast',
                 S_PLAYER_TAKE_OFF:'take_off',
                 S_PLAYER_DROP:'drop',
                 S_PLAYER_DRINK:'drink',
                 S_PLAYER_READ:'read',
                 S_PLAYER_IDENTIFY:'identify',
                 S_PLAYER_CURSOR: 'cursor',
                 S_PLAYER_STATS: 'stats'}

#quit messages
QUIT = 1
SAVE = 2

#move modes, have to be like map_tiles
MM_VOID = 0
MM_WALK = 1
MM_FLY = 2

#item-flags
IF_EQUIPABLE = 0x1
IF_DRINKABLE = 0x2
IF_EATABLE = 0x4
IF_READABLE = 0x8
IF_IDENTIFIED = 0x10
IF_SWORD = 0x20
IF_AXE = 0x40
IF_RANGED = 0x80
IF_MELEE = 0x100
IF_FIRES_ARROW = 0x200
IF_FIRES_BOLT = 0x400
IF_ARROW = 0x800
IF_BOLT = 0x1000
IF_FLAIL = 0x2000
IF_EXOTIC = 0x4000
IF_BOW = 0x8000
IF_CROSSBOW = 0x10000

#map-tile flags
F_WALKABLE = 0x1
F_FLYABLE = 0x2
#F_SWIMABLE = 0x4
F_BLOCKSIGHT = 0x8
#F_WALK_D = 0x10
#F_FLY_D = 0x20
#F_SWIN_D = 0x40
F_SC_UP = 0x80
F_SC_DOWN = 0x100
F_DIGABLE = 0x200
#F_LIT = 0x400
#F_SML_LIT = 0x800
F_MEMO = 0x1000

MAP_TILE_void = 9, 89, F_BLOCKSIGHT
MAP_TILE_bfloor = -1, 0, F_WALKABLE | F_FLYABLE
MAP_TILE_floor = 0, 1, F_WALKABLE | F_FLYABLE
MAP_TILE_wall = 1, 8 , F_BLOCKSIGHT | F_DIGABLE
MAP_TILE_door = 2, 32, F_WALKABLE | F_FLYABLE
MAP_TILE_down = 3, 42 , F_WALKABLE | F_SC_DOWN | F_FLYABLE
MAP_TILE_up = 4, 43 , F_WALKABLE | F_SC_UP | F_FLYABLE
  
MAP_TILE_LIST = [MAP_TILE_bfloor, MAP_TILE_void, MAP_TILE_floor, MAP_TILE_wall,
                 MAP_TILE_door, MAP_TILE_down, MAP_TILE_up]

def get_dis(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

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

def sort_by_type(a, b):
    return a.type - b.type

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

def get_new_pos(pos, direction):
    new_pos = pos        
    if direction == MOVE_DOWN or direction == MOVE_DOWN_LEFT or direction == MOVE_DOWN_RIGHT:
        new_pos = new_pos[0], new_pos[1] + 1
    if direction == MOVE_UP or direction == MOVE_UP_LEFT or direction == MOVE_UP_RIGHT:
        new_pos = new_pos[0], new_pos[1] - 1
    if direction == MOVE_RIGHT or direction == MOVE_DOWN_RIGHT or direction == MOVE_UP_RIGHT:
        new_pos = new_pos[0] + 1, new_pos[1] 
    if direction == MOVE_LEFT or direction == MOVE_DOWN_LEFT or direction == MOVE_UP_LEFT:
        new_pos = new_pos[0] - 1, new_pos[1]
    return new_pos

class Debug():
    
    game_instance = None
    
    @staticmethod
    def init_debug(game):
        Debug.game_instance = game
        
    @staticmethod
    def debug(text):
        if MES_SYS:
            if Debug.game_instance != None:
                Debug.game_instance.shout('[DEBUG-MESSGAE:] ' + text)
            #print text
