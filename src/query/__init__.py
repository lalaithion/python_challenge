#! python3

# Izaak Weiss, 2017

# standard library imports
import pprint
import sys

# local imports
import parser

pprint = pprint.PrettyPrinter().pprint

filters = []

def find(item, name):
    keys = name.split('.')
    for key in keys:
        ret = item.get(key, {})
    return str(ret)

def sift(item):
    for f in filters:
        if f[1] == '==':
            if find(item, f[0]) == f[2]:
                return True
        if f[1] == '!=' or f[1] == '<>':
            if find(item, f[0]) != f[2]:
                return True
    return False

def command(code, database):
    global filters
    try:
        ast = parser.parse(code)
    except Exception:
        print('There was an error parsing your query')
        return None
        
    if ast[0] == 'filter':
        if ast[1] == []:
            for f in filters:
                print(' '.join(f))
        else:
            for f in ast[1]:
                filters.append(f)

    elif ast[0] == 'list':
        print('IP', end='\t')
        for name in ast[1]:
            print(name, end='\t')
        print('')
        sifted = {key: True for key in database.keys()}
        for key, value in database.items():
            sifted[key] = sift(value)

        for key, value in sifted.items():
            if value == True:
                print(key, end='\t')
                for name in ast[1]:
                    print(find(database[key],name), end='\t')
                print('')

    elif ast[0] == 'clear':
        filters = []

def loop(database):
    pprint(database)
    while True:
        print('> ', end='')
        code = input()
        print(code)
        command(code, database)

if __name__ == '__main__':
    database = {100:{'a':'5', 'b':'7'},200:{'a':'100','b':'7'}}
    loop(database)
