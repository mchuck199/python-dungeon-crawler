#!/usr/bin/env python
#
#       run_game.py
#       
#       Copyright 2009 Dominic Kexel <dk@evil-monkey-in-my-closet.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       Part of (or All) the graphic tiles used in this program is the public 
#       domain roguelike tileset "RLTiles".
#       Some of the tiles have been modified by me.
#       You can find the original tileset at:
#       http://rltiles.sf.net

import sys
import os
import pickle
import gzip
import pygame

try:
    import psyco
    psyco.full()
    print "psyco found"
except:
    print "no psyco... maybe you should install it..."

sys.path.append(os.path.join('.', 'src'))

import engine
from pdcglobal import *

pygame.init()
screen = pygame.display.set_mode((800, 600))

if os.access('save.gz', os.F_OK):
    FILE=gzip.open('save.gz', 'r')
    game = pickle.load(FILE)
    game.screen=screen
    game.load_font()
    game.re_init()
    FILE.close()
else:   
    game = engine.Engine()


quit_mes = game.start()
print quit_mes

if quit_mes == SAVE:
    data = game 
    FILE=gzip.open('save.gz', 'w')
    pickle.dump(data, FILE, 2)
    FILE.close()

