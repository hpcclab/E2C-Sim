
from abc import ABCMeta,abstractmethod



class TaskType:

    __metaclass__ = ABCMeta

    
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    

