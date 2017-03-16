#! python3

# Izaak Weiss, 2017

# A class for representing an ip address more elegantly than as strings or tuples
class IpAddr:
    def __init__(self, data):
        self.tuple = tuple(map(int, data))
    
    def __contains__(self, i):
        return i in self.tuple
    
    def __getitem__(self, i):
        return self.tuple[i]
    
    def __str__(self):
        return '.'.join(map(str,self.tuple))
    
    def __repr__(self):
        return '<IpAddr: ' + str(self) + '>'
    
    def __iter__(self):
        yield from self.tuple
