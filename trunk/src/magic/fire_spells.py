from pdcresource import *
from pdcglobal import *
from magic import Spell

class FireSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = RED
        self.type = ST_GENERIC