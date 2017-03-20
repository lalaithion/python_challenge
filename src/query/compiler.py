#! python3

# Izaak Weiss, 2017

# standard library imports
import re
import pprint
from collections import namedtuple

pprint = pprint.PrettyPrinter().pprint

"""
> show [geoip.country, rdap.country, geoip.city] where (geoip.org == US)
> show [geoip.country, rdap.country, geoip.org] where (and (geoip.org == US) (geoip.list == hello world))
> show [geoip.country, rdap.country, geoip.org] where (or (geoip.country == US) (geoip.country == UK) (geoip.country == NL))

show SHOW epsilon
where WHERE epsilon
or || OR
and && AND
"""

regexes = {
    'show': r'show|Show|SHOW',
    'where': r'where|Where|WHERE',
    'or': r'or|\|\||OR|Or',
    'and': r'and|&&|AND|And',
    'eq': r'==|=|is',
    'neq': r'!=|<>|not',

    'whitespace': r'\s+',
    'comma': r',',
    'openb': r'\[',
    'closeb': r'\]',
    'openp': r'\(',
    'closep': r'\)',

    'symbol': r'[\w.]+',
}

class QuerySyntaxError(Exception):
    pass

Base = namedtuple('BasePredicate', ['symbol', 'comp', 'data'])
Predicate = namedtuple('Predicate', ['op', 'list'])
Code = namedtuple('Code', ['listable', 'predicate'])

def pop(string):
    Token = namedtuple('Token', ['type','text'])
    token = None
    rest = None
    for name, regex in regexes.items():
        match = re.match(regex, string)
        if match:
            token = match.group()
            rest = string[match.end():]
            break
    return Token(name, token), rest
    
def tokenize(line):
    original = line
    prev = line
    tokens = []
    while line != '':
        token, temp = pop(line)
        if temp == None:
            idx = original.find(line)
            print('Could not tokenize:')
            print(original[:idx], '\n', ' '*idx, original[idx:])
            return None
        line = temp
        tokens.append(token)
    return list(filter(lambda x: x[0] != 'whitespace', tokens))

def find_token(tokens, typ):
    for i in range(len(tokens)):
        if tokens[i].type == typ:
            return i
    return -1

def find_closep(tokens):
    count = 1
    index = 0
    while count > 0:
        index += 1;
        if index >= len(tokens):
            return -1
        if tokens[index].type == 'closep':
            count -= 1;
    return index

def parse_list(tokens):
    identifiers = []
    for i in tokens:
        if tokens[0].type == 'symbol':
            identifiers.append(tokens[0].text)
            tokens = tokens[1:]
        else:
            raise QuerySyntaxError('Syntax Error: identifiers must be separated by commas in the list')
        
        if tokens == []:
            break
        
        if tokens[0].type == 'comma':
            tokens = tokens[1:]
        else:
            raise QuerySyntaxError('Syntax Error: identifiers must be separated by commas in the list')
    return identifiers

def base_case(tokens):
    if len(tokens) != 3:
        print(tokens)
        raise QuerySyntaxError('Syntax Error: base predicates must consist of an identifier, a comparison, and a value')
    if tokens[0].type != 'symbol':
        raise QuerySyntaxError('Syntax Error: the first item in a base predicate must be an identifier')
    if tokens[1].type != 'eq' and tokens[1].type != 'neq':
        print(tokens[1])
        raise QuerySyntaxError('Syntax Error: the second item in a base predicate must be a comparison')
    if tokens[2].type != 'symbol':
        raise QuerySyntaxError('Syntax Error: the third item in a base predicate must be a value')
    
    return Base(tokens[0].text, tokens[1].type, tokens[2].text)

def operation_case(tokens):
    op = tokens[0].type
    lst = []
    tokens = tokens[1:]
    while tokens != []:
        if tokens[0].type != 'openp':
            raise QuerySyntaxError('Syntax Error: a predicate operation must be followed by a list of parentheis delimited predicates')
        else:
            tokens = tokens[1:]
            endex = find_closep(tokens)
            if endex == -1:
                print(tokens)
                raise QuerySyntaxError('Syntax Error: an open parenthesis was found without a matching close parenthesis')
            lst.append(parse_predicate(tokens[:endex]))
            tokens = tokens[endex+1:]
    return Predicate(op, lst)

def parse_predicate(tokens):
    if tokens[0].type == 'and' or tokens[0].type == 'or':
        return operation_case(tokens)
    elif tokens[0].type == 'symbol':
        return base_case(tokens)
    else:
        raise QuerySyntaxError('Syntax Error: a predicate must begin with an identifier or a predicate operation')

def parse(tokens):
    if tokens[0].type == 'show':
        tokens = tokens[1:]
    
    if tokens == []:
        return Code([],[])
    
    if tokens[0].type == 'openb':
        tokens = tokens[1:]
        idx = find_token(tokens,'closeb')
        if idx == -1:
            raise QuerySyntaxError('Syntax Error: An open square bracket was found without a matching close bracket')
        listables = parse_list(tokens[:idx])
        tokens = tokens[idx + 1:]
        
    if tokens == []:
        return Code(listables,[])
    
    if tokens[0].type == 'where':
        tokens = tokens[1:]
    
    if tokens[0].type == 'openp':
        tokens = tokens[1:]
        if tokens[-1].type != 'closep':
            raise QuerySyntaxError('Syntax Error: An open parenthesis was found without a matching close parenthesis')
        predicate = parse_predicate(tokens[:-1])
    
    return Code(listables, predicate)

def transform(line):
    tokens = tokenize(line)
    if tokens == None:
        return None

    pprint(tokens)
    print('\n\n')

    try:
        code = parse(tokens)
    except QuerySyntaxError as err:
        print(err)
        return None
    
    pprint(code)
    print('\n\n')

    return code
