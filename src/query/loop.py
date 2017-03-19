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
                res.append(str(item) + '\t')
            else:
                res.append('\t\t')
        res.append('\n')

    return res

def loop(database):
    while True:
        line = input(' > ')
        print(interpreter.run(line, database))

if __name__ == "__main__":
    loop({})
