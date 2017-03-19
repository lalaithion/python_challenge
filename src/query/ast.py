#! python3

# Izaak Weiss, 2017

# standard library imports
import re
from collections import namedtuple

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
    'orr': r'or|\|\||OR|Or',
    'andd': r'and|&&|AND|And',
    'eq': r'==|=|is',
    'neq': r'!=|<>|not',

    'whitespace': r'\s+',
    'comma': r',',
    'openb': r'\[',
    'closeb': r'\]',
    'openp': r'\(',
    'closep': r'\)',

    'ident': r'[\w.]+',
    'data': r'[^\(\)]+',
}

def pop(string):
    token = None
    rest = None
    for name, regex in regexes.items():
        match = re.match(regex, string)
        if match:
            token = match.group()
            rest = string[match.end():]
            break
    return (name, token), rest
    
def tokenize(line):
    original = line
    prev = line
    tokens = []
    while line != '':
        token, temp = pop(line)
        print(token)
        if temp == None:
            idx = original.find(line)
            print('Could not tokenize:')
            print(original[:idx], '\n', ' '*idx, original[idx:])
            return None
        line = temp
        tokens.append(token)
    return list(filter(lambda x: x[0] != 'whitespace', tokens))
        
def transform(line):
    return tokenize(line)
