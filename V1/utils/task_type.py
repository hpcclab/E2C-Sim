from abc import ABCMeta
from enum import Enum, unique


class TaskType:
    __metaclass__ = ABCMeta

    def __init__(self, id, name, urgency, deadline):
        self.id = id
        self.name = name
        self.urgency = urgency
        self.deadline = deadline
@unique
class UrgencyLevel(Enum):
    BESTEFFORT = 1
    URGENT = 2