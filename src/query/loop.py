#! python3

# Izaak Weiss, 2017

# standard library imports
import readline

# local imports
import query.interpreter as interpreter
import query.compiler as compiler

# take the list of lists and make it a marker deliniated string
def table(data, marker):
    res = ''

    # find the longest element in each column:
    buffers = [0 for i in range(len(data[0]))]
    for row in data:
        for index, item in enumerate(row):
            buffers[index] = max(buffers[index], len(str(item)))
        
    for row in data:
        for index, item in enumerate(row):
            if item:
                # justify it using spaces and a tab
                s = str(item)
                justify = buffers[index] - len(s)
                res += s + (' ' * justify) + marker
            else:
                # add enough spaces to make it equally spaced
                res += ' ' *  buffers[index] + marker
        # add newlines at the end of each row
        res += '\n'
        
    return res

# open a shell and run commands over and over
def loop(database):
    try:
        while True:
            line = input(' > ')
            data = interpreter.run(line, database)
            if type(data) == compiler.Quit:
                break
            if data != None:
                print(table(data, '\t'))
    except EOFError:
        print('')
        return

# run a single command on a databse
def command(database, command, marker='\t'):
    data = interpreter.run(command, database)
    return table(data, marker)

if __name__ == "__main__":
    # sample dumb database for my own testing
    loop({
        '10.2.2.2': {'love':{'baby': 100000000000000000, 'fish':12}, 'hurt':{'tomorrow':-1, 'today':12, 'yesterday':0}, 'this':5},
        '23.4.5.6': {'love':{'baby': 9, 'fish':13}, 'hurt':{'tomorrow':1, 'today':13, 'yesterday':0}, 'this':2},
        '1.2.3.4': {'love':{'baby': 9, 'fish':12}, 'hurt':{'tomorrow':-10, 'today':14, 'yesterday':0}, 'this':7},
        '103.2.255.6': {'love':{'baby': 9, 'fish':12}, 'hurt':{'tomorrow':0, 'today':12, 'yesterday':0}, 'this':1}
    })
