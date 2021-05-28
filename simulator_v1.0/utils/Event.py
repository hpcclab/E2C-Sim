
from enum import Enum, unique

class Event:
    # An event explains different stages of processing a task, from
    # arriving to completing the task.
    #
    # event_type: The stage of processing a task like "arriving" or 
    # "completing" 
    # time: It is the time of occuring an event. For example,
    # time of arriving a task in "arriving" event.
    # event_details: a dictionary that describes the event in detail.
    
    def __init__(self, time , event_type, event_details):        
        self.time = time
        self.event_type = event_type
        self.event_details = event_details
        
    def __eq__(self, other):
        return self.time == other.time
    
    def __ne__(self, other):
        return self.time != other.time
    
    def __lt__(self,other):
        return self.time < other.time
    
    def __le__(self,other):
        return self.time <= other.time
    
    def __gt__(self,other):
        return self.time > other.time       
    
    def __ge__(self,other):
        return self.time >= other.time

class EventTypes(Enum):
    ARRIVING = 1
    COMPLETION = 2
    