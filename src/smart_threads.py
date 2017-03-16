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
        global thread_count
        thread_count += 1
        if name == None:
            name = 'Thread ' + str(thread_count)
        self.box = Box(None)
        intermediate_args = (self.box, target, args, kwargs)
        self.thread = threading.Thread(target = thread_return,
                         name = name, args = intermediate_args,
                         daemon = True)
        self.thread.start()

    def join(self):
        self.thread.join()
        return self.box.value
