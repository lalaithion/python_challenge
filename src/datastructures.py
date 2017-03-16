#! python3

# Izaak Weiss, 2017

# A class for representing an ip address more elegantly than as strings or tuples
class IpAddr:
    def __init__(self, data):
        self.tuple = tuple(map(int, data))
    
    # who knows, may be useful
    def __contains__(self, i):
        return i in self.tuple
    
    # so we can write ip[2] instead of ip.tuple[2]
    def __getitem__(self, i):
        return self.tuple[i]
    
    # str and repr are must haves for any class
    def __str__(self):
        return '.'.join(map(str,self.tuple))
    
    def __repr__(self):
        return '<IpAddr: ' + str(self) + '>'
    
    # lets us cast this to a tuple or list easily
    def __iter__(self):
        yield from self.tuple
    
    # equaity seems important
    def __eq__(self, other):
        try:
            return self.tuple == other.tuple
        except:
            return NotImplemented
    
    def __ne__(self, other):
        try:
            return self.tuple != other.tuple
        except:
            return NotImplemented
    
    # hashing is required for **nice** usage in sets and dictionaries
    def __hash__(self):
        return hash(self.tuple)
