from abc import ABCMeta, abstractmethod


class TaskType:
    __metaclass__ = ABCMeta

    def __init__(self, id, name, urgency, deadline):
        self.id = id
        self.name = name
        self.urgency = urgency
        self.deadline = deadline
