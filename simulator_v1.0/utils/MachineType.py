
from abc import ABCMeta,abstractmethod



class MachineType:

    __metaclass__ = ABCMeta

    
    def __init__(self, id, name, power, replicas):
        self.id = id
        self.name = name
        self.power = power
        self.replicas = replicas
    

