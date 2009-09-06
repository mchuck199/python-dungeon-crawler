import random

def SmallRusty(item):
    item.name='Rusty ' +item.name
    if item.min_damage>1:
        item.min_damage-=1
    item.max_damage-=random.randint(1,2)
    

def SmallBeggars(item):
    item.name='Beggar\'s ' +item.name
    if item.av > 10:
        item.av-=10

def SmallBrutal(item):
    item.name='Brutal ' +item.name
    item.min_damage+=random.randint(1,2)
    item.max_damage+=random.randint(2,3)