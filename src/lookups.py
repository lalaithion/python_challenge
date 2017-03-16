#! python3

# Izaak Weiss, 2017

# standard library imports
import random

# third party imports
import requests

def geoip(ip_addr):
    urlstr = 'http://ipinfo.io/' + str(ip_addr) + '/json'
    req = requests.get(urlstr)
    if req.status_code != requests.codes.ok:
        return {}
    return req.json()

def rdap(ip_addr):
    urlstr = 'http://rdap.apnic.net/ip/' + str(ip_addr)
    req = requests.get(urlstr)
    if req.status_code != requests.codes.ok:
        return {}
    return req.json()
