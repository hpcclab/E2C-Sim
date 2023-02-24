"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 20, 2022

"""

from enum import Enum, unique


class Event:
   

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
    STARTED = 1
    FINISHED = 2
