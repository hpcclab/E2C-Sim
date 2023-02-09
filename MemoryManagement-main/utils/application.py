"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022

"""

from enum import Enum, unique
from functools import total_ordering


@total_ordering
class Application:

    def __init__(self, name, models):
        self.name = name
        self.models =  models
        self.status = AppStatus.MINIMAL
        self.start_time = None
        self.finish_time = None
        self.evict_time = None
        self.loaded_model_size = 0
        self.prt = []
        self.nxt_rq = None
        self.stats = {'requested_times': [], 
                        'finish_times':[],
                        'evicted_times':[],
                        'allocated_memory':[],                       
                    }
        self.timeseries = {'time':[0],
        'allocated_memory':[0]}
    
    def __gt__(self, other):
        return self.loaded_model_size > other.loaded_model_size   
    
@unique
class AppStatus(Enum):    
    MINIMAL = 2
    AGGRESSIVE = 3
    