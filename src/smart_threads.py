#! python3

# Izaak Weiss, 2017

# standard library imports
import threading

thread_count = 0

# Sort of a python pointer to a value. This lets me treat any value as mutable-ish
class Box:
    def __init__(self, value):
        self.value = value

# store the return value of your function in an accessible place
def thread_return(ret, f, args, kwargs):
    ret.value = f(*args, **kwargs)

# this class wraps a thread in an interface that makes .join() return the return
# value of the function that was passed in as target
class SmartThread:
    def __init__(self, target = lambda: None, name = None, args = (), kwargs = {}):
        # keep track of the number of threads for default naming
        global thread_count
        thread_count += 1
        # if the name is none, give it a default name
        if name == None:
            name = 'SmartThread ' + str(thread_count)
        # the box is a place to store the return value
        self.box = Box(None)
        # these arguments are the arguments to thread_return, not to target
        intermediate_args = (self.box, target, args, kwargs)
        #make a thread
        self.thread = threading.Thread(target = thread_return,
                         name = name, args = intermediate_args,
                         daemon = True)
    
    # start the thread
    def start(self):
        self.thread.start()
        return self

    # when you join the thread, we also retrieve it's return value.
    def join(self):
        self.thread.join()
        return self.box.value

    # str and repr are must haves for any class
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return '<SmartThread: ' + self.name + '>'
