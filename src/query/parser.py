#! python3

# Izaak Weiss, 2017

# standard library imports
import re

# filter
#   lists all filters
# filter geoip.country == 'NL'
#   adds a filter of geoip.country == 'NL'
# list
#   lists all ips, subject to filters
# list ip, geoip.country
#   lists all ips and their countries, subject to filters
# clear
#   clears all filters

filter_re = re.compile(r'\bfilter\b')
list_re = re.compile(r'\blist\b')
clear_re = re.compile(r'\bclear\b')

item_re = re.compile(r'\b[\w.]*\b')
data_re = re.compile(r'".*?"|\'.*?\'')
op_re = re.compile(r'==|!=|<>')

whitespace_re = re.compile(r'\s*')
comma_re = re.compile(r',')

def strip(code, match):
    code = code[match.end():]
    code = code[whitespace_re.match(code).end():]
    return code

def parse_filter(code):
    filter_ls = []
    
    if whitespace_re.fullmatch(code):
        return filter_ls
    
    while True:
        # match and pull out the item
        match = item_re.match(code)
        item = code[:match.end()]
        code = strip(code, match)
        
        # match and pull out the operation
        match = op_re.match(code)
        op = code[:match.end()]
        code = strip(code, match)
        
        # match and pull out the data
        match = data_re.match(code)
        data = code[:match.end()]
        data = data[1:-1]
        code = strip(code, match)
        
        # append this filter to list
        filter_ls.append([item, op, data])
        
        # see if there's another filter
        match = comma_re.match(code)
        if match is None:
            break
        code = strip(code, match)

    if whitespace_re.fullmatch(code):
        return filter_ls
    else:
        raise ValueError

def parse_list(code):
    list_ls = []
    
    if whitespace_re.fullmatch(code):
        return list_ls
    
    while True:
        # match and pull out the item
        match = item_re.match(code)
        item = code[:match.end()]
        code = strip(code, match)
        
        # append this filter to list
        list_ls.append(item)
        
        # see if there's another filter
        match = comma_re.match(code)
        if match is None:
            break
        code = strip(code, match)

    if whitespace_re.fullmatch(code):
        return list_ls
    else:
        raise ValueError

def parse(code):
    match = filter_re.match(code)
    if match:
        code = strip(code, match)
        return ('filter', parse_filter(code))

    match = list_re.match(code)
    if match:
        code = strip(code, match)
        return ('list', parse_list(code))

    match = clear_re.match(code)
    if match:
        code = strip(code, match)
        if whitespace_re.fullmatch(code):
            return ('clear',)
        else:
            raise ValueError
    return None