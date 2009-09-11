import random

def SmallRusty(item):
    item.full_name = 'Rusty ' + item.full_name
    if item.min_damage > 1:
        item.min_damage -= 1
    item.max_damage -= random.randint(1, 2)
    

def SmallBeggars(item):
    item.full_name = 'Beggar\'s ' + item.full_name
    if item.av > 10:
        item.av -= 10

def SmallBrutal(item):
    item.full_name = 'Brutal ' + item.full_name
    item.min_damage += random.randint(1, 2)
    item.max_damage += random.randint(2, 3)
