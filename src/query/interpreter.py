#! python3

# Izaak Weiss, 2017

# local imports
import ast

def run(line, database):
    code = ast.transform(line)
    return code
