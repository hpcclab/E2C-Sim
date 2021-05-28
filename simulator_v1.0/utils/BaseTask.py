from abc import ABCMeta,abstractmethod
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
    PENDING = 2
    RUNNING = 3
    COMPLETED = 4
    OFFLOADED = 5
    DROPPED = 6
    DEFERRED = 7
    MISSED = 8

