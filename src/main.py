#! python3

# Izaak Weiss, 2017

# standard library imports
import fileinput
import json
import argparse
import readline

# local imports
import ip_parser
import lookups
import smart_threads as st
from datastructures import IpAddr
import query.interpreter as interpreter
import query.compiler as compiler

# utility function to 'zip' two dictionaries where their keys overlap
def dict_zip(d1, d2):
    ret = {}
    for key, value in d1.items():
        if key in d2.keys():
            ret[key] = (value, d2[key])
    return ret
    
# save dictionary to json file
def save(database, filename):
    with open(filename, 'w') as dbfile:
        json.dump(database,dbfile,indent=2)

# load the output of the previous function
def load(filename):
    with open(filename, 'r') as dbfile:
        database = json.load(dbfile)
    database = {IpAddr.from_string(key): value for key, value in database.items()}
    return database

def parse_and_lookup(files, output):
    ip_ls = []
    # loop over stdin or lines from files supplied as command line arguments
    for line in fileinput.input(files):
        # append any ip addresses that occur in the line
        ip_ls += ip_parser.ip_addrs(line)
    
    # uniquify the list, for performance reasons
    ip_ls = list(set(ip_ls))
    
    geoip_threads = {}
    rdap_threads = {}
    # spawn worker threads to handle each ip address
    # this operation is io bound, so it doesn't matter if we have
    # more threads than cores
    for ip in ip_ls:
        geoip_threads[ip] = st.SmartThread(target = lookups.geoip,
                                name = 'GeoIP Lookup for ' + str(ip),
                                args = (ip,)).start()
        rdap_threads[ip] = st.SmartThread(target = lookups.rdap,
                                name = 'RDAP Lookup for ' + str(ip),
                                args = (ip,)).start()
    
    # join threads and gather info from them
    geoip_info = {}
    for ip, thread in geoip_threads.items():
        geoip_info[ip] = thread.join()
        
    rdap_info = {}
    for ip, thread in rdap_threads.items():
        rdap_info[ip] = thread.join()
    
    # put data into a nice structure
    info = {key: {'geoip': value[0], 'rdap': value[1]}
            for key, value in dict_zip(geoip_info, rdap_info).items()}
    
    # save the databse
    save(info, output)
    
    return info
    
def load_database(files):
    # loop over input files, loading them into a database
    info = {}
    for f in files:
        info.update(load(f))
    
    return info
    
# open a shell and run commands over and over
def loop(database):
    try:
        while True:
            line = input(' > ')
            data = interpreter.run(line, database)
            if type(data) == compiler.Quit:
                break
            if data != None:
                print(interpreter.table(data, '\t'))
    except EOFError:
        print('')
        return

# run a single command on a databse
def command(database, command, marker='\t'):
    data = interpreter.run(command, database)
    return interpreter.table(data, marker)

# handle command line arguments here
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='*', default=['-'],
        help='Files to read, if empty, stdin is used.')
    parser.add_argument('-o', '--output', dest='output', default='database.json',
        help='Specify the output file.')
    parser.add_argument('-l', '--load', dest='load', action='store_true',
        help='If present, it treats the input files as json files output by this tool.')
    parser.add_argument('-c', '--command', dest='command', default=None, const='', nargs='?',
        help='If present, no shell is opened and the command after it is run instead, \
        with the result output. No command will simply print all IP adresses.')
    args = parser.parse_args()
    
    if args.load:
        info = load_database(args.files)
    else:
        info = parse_and_lookup(args.files, args.output)
    
    if args.command == None:
        loop(info)
    else:
        print(command(info,args.command), end='')
