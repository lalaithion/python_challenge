#! python3

# Izaak Weiss, 2017

# standard library imports
import pprint
import sys

# local imports
import query.parser

pprint = pprint.PrettyPrinter().pprint

filters = []

# find an item based on a name
def find(item, name):
    # the name is a list of keys
    keys = name.split('.')
    # for each key, go deeper into the dictionary
    for key in keys:
        item = item.get(key, {})
    
    # if nothing is found, return a tab; else return the item
    if item == {}:
        return '\t'
    else:
        return str(item)

# find if an item satisfies all filters; aka sift it.
def sift(item):
    global filters
    # by default, everythign is true.
    status = True
    for f in filters:
        # there's an equals and a not equals case
        # then we set status to false and break out if it fails a filter
        if f[1] == '==':
            if not find(item, f[0]) == f[2]:
                status = False
                break
        if f[1] == '!=' or f[1] == '<>':
            if not find(item, f[0]) != f[2]:
                status = False
                break

    return status

def command(code, database):
    global filters
    
    # try parsing an AST
    try:
        ast = parser.parse(code)
    except Exception:
        print('There was an error parsing your query')
        return {}
    
    # add a filter if there was a filter command. If there's no following
    # aruments, print all the filters
    if ast[0] == 'filter':
        if ast[1] == []:
            for f in filters:
                print(' '.join(f))
        else:
            for f in ast[1]:
                filters.append(f)

    elif ast[0] == 'list':
        # print headers
        print('IP', end='\t')
        for name in ast[1]:
            print(name, end='\t')
        print('')
        # figure out which IPs to show
        sifted = {key: True for key in database.keys()}
        for key, value in database.items():
            sifted[key] = sift(value)

        # print out data requested for the IPs that should be shown
        for key, value in sifted.items():
            if value == True:
                print(key, end='\t')
                for name in ast[1]:
                    print(find(database[key],name), end='\t')
                print('')

    # clear all filters
    elif ast[0] == 'clear':
        filters = []

def loop(database):
    while True:
        # repl
        print('> ', end='')
        code = input()
        command(code, database)
