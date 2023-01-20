"""
Authors: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 26, 2022

Description:


"""
"""
Authors: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 26, 2022

Description:


"""
import sys 

class Queue:

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.list = []
        
    def qsize(self):
        return len(self.list)

    def empty(self):
        return not bool(self.list)
    
    def full(self):
        return self.qsize() == self.maxsize
    
    def put(self, item):        
        try:
            if self.full():
                raise FullQueueError(item)
            else:
                self.list.append(item)
        except FullQueueError as err:
            print(err)
            sys.exit()
    
    def insert(self, index, item):        
        try:
            if self.full():
                raise FullQueueError(item)
            else:
                self.list.insert(index, item)
        except FullQueueError as err:
            print(err)
            sys.exit()
    
    def get(self, index = 0):                
        try:
            self.list[index]                   
        except IndexError as val_err:
            print(val_err)
            print(f'index {index} is out of range of list {self.list}')
            sys.exit()
        return self.list.pop(index)
        
        
    
    def remove(self, item):
        try:
            index = self.list.index(item)            
        except ValueError as err:            
            print(err)
            sys.exit()        
        self.list.pop(index)
        


class FullQueueError(Exception):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f'FullQueueError: Try to put {self.item} to the full queue'

class EmptyQueueError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'EmptyQueueError: Try to get item from an empty queue'
        
    
    


    