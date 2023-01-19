from abc import ABCMeta, abstractmethod
from enum import Enum, unique


class BaseTask:
    __metaClass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def info(self):
        """ it gives the details about the task

            Returns:
                a dictionary that includes: id, type, status, assigned machine if
                it is mapped, etc.

        """


@unique
class TaskStatus(Enum):
    ARRIVING = 1
    CANCELLED = 2
    PENDING = 3
    RUNNING = 4
    COMPLETED = 5
    XCOMPLETED = 6 # BE tasks completed in devaluation window
    OFFLOADED = 7    
    DEFERRED = 9
    MISSED = 10
    PREEMPTED = 11
