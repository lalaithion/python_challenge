#! python3

# Izaak Weiss, 2017

# standard library imports
import fileinput
from collections import namedtuple

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
                                args = (ip,))
        rdap_threads[ip] = st.SmartThread(target = lookups.rdap,
                                name = 'RDAP Lookup for ' + str(ip),
                                args = (ip,))
    
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
    
    # enter into a query loop regarding the information
    query.loop(info)

if __name__ == '__main__':
    main()
