#! python3

# Izaak Weiss, 2017

# standard library imports
import random

# third party imports
import requests

def geoip(ip_addr):
    # create a request string
    urlstr = 'http://ipinfo.io/' + str(ip_addr) + '/json'
    # make the request
    req = requests.get(urlstr)
    # check for errors
    if req.status_code != requests.codes.ok:
        return {}
    # return the data as a dictionary
    return req.json()

def rdap(ip_addr):
    # create a request string
    urlstr = 'http://rdap.apnic.net/ip/' + str(ip_addr)
    # make the request
    req = requests.get(urlstr)
    # check for errors
    if req.status_code != requests.codes.ok:
        return {}
    # return the data as a dictionary
    return req.json()
