#! python3

# Izaak Weiss, 2017

# standard library imports
import re

# local imports
from datastructures import IpAddr

# each ip num can be between 0 and 255; here's a regex way of saying that.
ip_num = r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])'
# an ip addr is 4 ip nums separated by spaces.
ip_addr = ip_num + r'\.' + ip_num + r'\.' + ip_num + r'\.' + ip_num
ip_regex = re.compile(ip_addr)

# Izaak Weiss, 2017
def ip_addrs(string):
    # find all ip addresses and map them to IpAddr objects
    ip_list = map(IpAddr, ip_regex.findall(string))
    return ip_list
