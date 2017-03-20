#! python3

# Izaak Weiss, 2017

# standard library imports
from functools import reduce
from ast import literal_eval

# local imports
import compiler


def resolve(obj, ident):
    keyls = ident.split('.')
    for key in keyls:
        obj = obj.get(key, {})
    return obj

def base_sieve(obj, pred):
    data = resolve(obj, pred.symbol)
    print(data)
    if pred.comp == 'eq':
        return data == literal_eval(pred.data)
    else:
        return data != literal_eval(pred.data)

def sieve(obj, filters):
    if filters == []:
        return True
    elif type(filters) == compiler.Base:
        return base_sieve(obj, filters)
    else:
        if filters.op == 'and':
            f = lambda x, y: x and y
        else:
            f = lambda x, y: x or y
        return reduce(f, map(sieve, filters.list))

def display(code, database):
    rows = [['IP'] + [ident for ident in code.listable]]
    for ip, obj in database.items():
        current = []
        if sieve(obj, code.predicate):
            current.append(ip)
            for ident in code.listable:
                current.append(resolve(obj, ident))
            rows.append(current)
    return rows

def run(line, database):
    code =  compiler.transform(line)
    disp = display(code, database)
    compiler.pprint(disp)
    print('\n\n')

    return disp
