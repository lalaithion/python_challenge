#! python3

# Izaak Weiss, 2017

# WARNING
# This version should never be used if the other main function can be.
# This version has no multithreading, and as such is about 5 times slower.
# It was created for testing purposes and may not be up to date with the
# features available in main.py
# END WARNING

# standard library imports
import fileinput
import json

# local imports
import parser
import lookups
import query
import smart_threads as st

# utility function to 'zip' two dictionaries where their keys overlap
def dict_zip(d1, d2):
    ret = {}
    for key, value in d1.items():
        if key in d2.keys():
            ret[key] = (value, d2[key])
    return ret
    
def save(database):
    with open('database.json', 'w') as dbfile:
        json.dump(database,dbfile,indent=2)

def load(file):
    pass

def main():
    ip_ls = []
    # loop over stdin or lines from files supplied as command line arguments
    for line in fileinput.input():
        # append any ip addresses that occur in the line
        ip_ls += parser.ip_addrs(line)
    
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
    for ip in ip_ls:
        geoip_info[ip] = lookups.geoip(ip)
        
    rdap_info = {}
    for ip in ip_ls:
        rdap_info[ip] = lookups.rdap(ip)
    
    # put data into a nice structure
    info = {key: {'geoip': value[0], 'rdap': value[1]}
            for key, value in dict_zip(geoip_info, rdap_info).items()}
    
    save(info)
    
    # enter into a query loop regarding the information
    query.loop(info)


if __name__ == '__main__':
    main()
