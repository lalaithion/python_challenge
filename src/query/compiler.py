#! python3

# Izaak Weiss, 2017

# standard library imports
import re
import pprint
from collections import namedtuple

pprint = pprint.PrettyPrinter().pprint

verbose = False

# regexes used to tokenize
regexes = {
    'quit': r'q|Q|quit|Quit|QUIT',
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

# custom error for me to catch
class QuerySyntaxError(Exception):
    pass

# type used for tokenizing code
Token = namedtuple('Token', ['type','text'])
# types used in the AST for the code
Base = namedtuple('BasePredicate', ['symbol', 'comp', 'data'])
Predicate = namedtuple('Predicate', ['op', 'list'])
Code = namedtuple('Code', ['listable', 'predicate'])
Quit = namedtuple('Quit', [])

# takes a string and pops a token off of it.
def pop(string):
    token = None
    rest = None
    # for each regex
    for name, regex in regexes.items():
        # try and match the regex to the beginning of the string
        match = re.match(regex, string)
        if match:
            # if we matched, put the token string and the remaining string into variables
            token = match.group()
            rest = string[match.end():]
            # exit the loop
            break
    return Token(name, token), rest

# loop over the string, popping off tokens until nothing is left
def tokenize(line):
    original = line
    prev = line
    tokens = []
    while line != '':
        token, temp = pop(line)
        # temp is none if the pop failed; print error message
        if temp == None:
            idx = original.find(line)
            print('Could not tokenize:')
            print(original[:idx], '\n', ' '*idx, original[idx:])
            return None
        line = temp
        tokens.append(token)
    # remove whitespace tokens from list before returning
    return list(filter(lambda x: x[0] != 'whitespace', tokens))

# helper function to find a specific type of token
def find_token(tokens, typ):
    for i in range(len(tokens)):
        if tokens[i].type == typ:
            return i
    return -1

# helper function to find matching close parenthesis.
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

# function to parse the [] list in the line
def parse_list(tokens):
    identifiers = []
    for i in tokens:
        # we try and pop off a symbol here
        if tokens[0].type == 'symbol':
            identifiers.append(tokens[0].text)
            tokens = tokens[1:]
        else:
            raise QuerySyntaxError('Syntax Error: identifiers must be separated by commas in the list')
        
        # if there is nothing left, we can exit the loop here
        if tokens == []:
            break
        
        # we require a comma before the next item
        if tokens[0].type == 'comma':
            tokens = tokens[1:]
        else:
            raise QuerySyntaxError('Syntax Error: identifiers must be separated by commas in the list')
    return identifiers

# base case for predicate parsing
def base_case(tokens):
    # we require three tokens with the right types:
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
    
    # return a Base with the right data; we know the data is valid from the above checks
    return Base(tokens[0].text, tokens[1].type, tokens[2].text)

# recursive case for predicates
def operation_case(tokens):
    # the operation is the first token's type
    op = tokens[0].type
    lst = []
    tokens = tokens[1:]
    # until we have nothing left...
    while tokens != []:
        # we have to have a parenthesis
        if tokens[0].type != 'openp':
            raise QuerySyntaxError('Syntax Error: a predicate operation must be followed by a list of parentheis delimited predicates')
        else:
            tokens = tokens[1:]
            # find the matching close parenthesis
            endex = find_closep(tokens)
            if endex == -1:
                print(tokens)
                raise QuerySyntaxError('Syntax Error: an open parenthesis was found without a matching close parenthesis')
            # parse the tokens inside the parenthesis, and append them to the list
            lst.append(parse_predicate(tokens[:endex]))
            tokens = tokens[endex+1:]
    # return the predicate
    return Predicate(op, lst)

# main predicate function
def parse_predicate(tokens):
    # if the predicate begins with an operation, use that case
    if tokens[0].type == 'and' or tokens[0].type == 'or':
        return operation_case(tokens)
    # otherwise, use the base case
    elif tokens[0].type == 'symbol':
        return base_case(tokens)
    # other otherwise, throw an error
    else:
        raise QuerySyntaxError('Syntax Error: a predicate must begin with an identifier or a predicate operation')

# main parsing function
def parse(tokens):
    listables = []
    predicate = []
    
    # if empty, return here
    if tokens == []:
        return Code([],[])
    
    # see if the command is quit
    if tokens[0].type == 'quit':
        return Quit()
    
    # optionally find a show command
    if tokens[0].type == 'show':
        tokens = tokens[1:]
    
    # if empty, return here
    if tokens == []:
        return Code([],[])
    
    # if open bracket exists, parse list
    if tokens[0].type == 'openb':
        tokens = tokens[1:]
        idx = find_token(tokens,'closeb')
        if idx == -1:
            raise QuerySyntaxError('Syntax Error: An open square bracket was found without a matching close bracket')
        listables = parse_list(tokens[:idx])
        tokens = tokens[idx + 1:]
        
    # if empty, return here
    if tokens == []:
        return Code(listables,[])
    
    # optionally find a where command
    if tokens[0].type == 'where':
        tokens = tokens[1:]
    
    # if parenthesis exists, parse predicate
    if tokens[0].type == 'openp':
        tokens = tokens[1:]
        if tokens[-1].type != 'closep':
            raise QuerySyntaxError('Syntax Error: An open parenthesis was found without a matching close parenthesis')
        predicate = parse_predicate(tokens[:-1])
    
    # return full code
    return Code(listables, predicate)

# main compiler function
def transform(line):
    # tokenize, check for errors
    tokens = tokenize(line)
    if tokens == None:
        return None

    # if verbose (default false) print stuff
    if verbose:
        pprint(tokens)
        print('\n\n')

    # try parsing; if error, catch it and print it, returning None
    try:
        code = parse(tokens)
    except QuerySyntaxError as err:
        print(err)
        return None

    # if verbose (default false) print stuff
    if verbose:
        pprint(code)
        print('\n\n')

    # return successful code
    return code
