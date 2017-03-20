#! python3

# Izaak Weiss, 2017

# standard library imports
from functools import reduce
from ast import literal_eval

# local imports
import query.compiler as compiler

# resolve a value in the object by making it a list of keys, and recursively accessing those keys
def resolve(obj, ident):
    keyls = ident.split('.')
    for key in keyls:
        obj = obj.get(key, {})
    return obj

# sieve an object based on a base predicate
def base_sieve(obj, pred):
    # resolve the data in the object
    data = resolve(obj, pred.symbol)

    # try evaluating the pred.data, if that fails, it's a string
    try:
        value = literal_eval(pred.data)
    except:
        value = pred.data
    
    # comapre them based on operation
    if pred.comp == 'eq':
        return data == value
    else:
        return data != value

# sieve an object based on any filter
def sieve(obj, filters):
    # no filters means it passes all of them
    if filters == []:
        return True
    # if this is a base filter, call base_sieve
    elif type(filters) == compiler.Base:
        return base_sieve(obj, filters)
    # otherwise it's a compund predicate
    else:
        # define a function f to perform the and or or operation
        if filters.op == 'and':
            f = lambda x, y: x and y
        else:
            f = lambda x, y: x or y
        # use reduce and map to sieve the values (yay functional programming)
        return reduce(f, map(lambda f: sieve(obj, f), filters.list))

def display(code, database):
    if type(code) == compiler.Quit:
        return code
    # create the header values
    rows = [['IP'] + [ident for ident in code.listable]]
    # for each object
    for ip, obj in database.items():
        current = []
        # if it passes the filters
        if sieve(obj, code.predicate):
            # append the ip
            current.append(ip)
            # and any identifiers in the list
            for ident in code.listable:
                current.append(resolve(obj, ident))
            rows.append(current)
    return rows

def run(line, database):
    # try and compile the code
    code =  compiler.transform(line)
    # if it worked, put it into a displayabale format
    if code != None:
        return display(code, database)

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
