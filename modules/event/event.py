"""
Authors: Ali Mokhtari, Chavit Denninnart
Created on Dec. 18, 2020.

Description: 

"""

from enum import Enum


class Event:
    # Description:

    def __init__(self, time, event_type, event_details):
        self.time = time
        self.event_type = event_type
        self.event_details = event_details

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return self.time != other.time

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time


class EventTypes(Enum):
    # Description: 
    ARRIVING = 1
    COMPLETION = 2
    DROPPED_RUNNING_TASK = 3
    DEFERRED = 4
    OFFLOADED = 5
