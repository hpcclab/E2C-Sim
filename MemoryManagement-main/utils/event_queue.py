"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 20, 2022

"""
import heapq

from utils.event import Event


class EventQueue:
    
    event_list = []

    def add_event(self, event):
        # Insert an event into the event_list.
        if isinstance(event, Event):
            heapq.heappush(self.event_list, event)

    def get_first_event(self):
        # it returns the root of event_list which is the event with 
        # smallest time.

        if self.event_list:  # it checks that event_list is non-empty
            return heapq.heappop(self.event_list)
        else:
            return Event(None, None, None)

    def remove(self, event):
        # It removes the event from the event_list. Then, the resulted
        # event_list is heapified again.         
        self.event_list.remove(event)
        heapq.heapify(self.event_list)
    
    def reset(self):
        self.event_list = []
