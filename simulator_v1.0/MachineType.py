
from abc import ABCMeta,abstractmethod



class MachineType:

    __metaclass__ = ABCMeta

    
    def __init__(self, id, name, power):
        self._id = id
        self._name = name
        self._power = power
    

