"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 16, 2022

"""
import sys


class Memory:

    def __init__(self, size):        
        self.size = size
        self.used = 0
        self.free = self.size - self.used

    
    def init(self, size):
        self.size = size
        self.used = 0
        self.free = self.size - self.used

    def free_size(self):
        return self.free
    
    def allocate(self, value):
        # try:
        #     assert(self.free >= value), f'ERROR[memory.py -> allocate()]: The requested memory size is not available' 
        # except AssertionError as err_msg:
        #     print(err_msg)            
        #     sys.exit()        
        self.free -= value
        self.used += value
    
    def release(self, value):
        self.free += value
        self.used -= value


def test():
    mem = Memory()
    mem.init()
    print( f'The memory size is {mem.size} MB')
    mem.allocate(5000)
    print(f'The free memory size is {mem.free}')

# test
if __name__ == '__main__':
    test()