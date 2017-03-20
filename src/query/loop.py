#! python3

# Izaak Weiss, 2017

# standard library imports
import readline

# local imports
import interpreter

def table(data):
    res = ''

    for row in data:
        for item in row:
            if item:
                res += str(item) + '\t'
            else:
                res += '\t\t'
        res += '\n'

    return res

def loop(database):
    while True:
        line = input(' > ')
        print(table(interpreter.run(line, database)))

if __name__ == "__main__":
    loop({
        '10.2.2.2': {'love':{'baby': 10, 'fish':12}, 'hurt':{'tomorrow':-1, 'today':12, 'yesterday':0}, 'this':5},
        '23.4.5.6': {'love':{'baby': 9, 'fish':13}, 'hurt':{'tomorrow':1, 'today':13, 'yesterday':0}, 'this':2},
        '1.2.3.4': {'love':{'baby': 9, 'fish':12}, 'hurt':{'tomorrow':-10, 'today':14, 'yesterday':0}, 'this':7},
        '103.2.255.6': {'love':{'baby': 9, 'fish':12}, 'hurt':{'tomorrow':0, 'today':12, 'yesterday':0}, 'this':1}
    })
