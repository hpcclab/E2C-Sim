"""
Authors: Ali Mokhtari, Chavit Denninnart
Created on Dec. 18, 2020.

Description: 

"""
import heapq

from modules.event.event import Event

class EventQueue:
    # Description

    event_list = []

    def add_event(self, event):   
        # Method Description:     
        if isinstance(event, Event):
            heapq.heappush(self.event_list, event)

    def get_first_event(self):
        # Method Description:
        if self.event_list:  
            return heapq.heappop(self.event_list)
        else:
            return Event(None, None, None)

    def remove(self, event):
        # Method Description:        
        self.event_list.remove(event)
        heapq.heapify(self.event_list)
    
    def reset(self):
        # Method Description:
        self.event_list = []
