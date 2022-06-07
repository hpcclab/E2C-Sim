
from abc import ABCMeta, abstractmethod
from enum import Enum, unique


@unique
class MachineStatus(Enum):
    OFF = 0
    WORKING = 1
    IDLE = 2


class BaseMachine:
    __metaclass__ = ABCMeta

    def __init__(self, id, type, specs):
        pass

    @abstractmethod
    def start(self):
        """ it starts the machine and make it ready to admit tasks

            Note:
                It should change the machine's status

        """

    @abstractmethod
    def admit(self, task):
        """ it assigns the task to the machine. That is, the task is appended
        to the machine queue

            Note:
                the machine available time should be updated here.

        """

    @abstractmethod
    def select(self):
        """ It selects a task from queue for running

           
            Returns:
                the selected task object

        """

    @abstractmethod
    def execute(self, index):
        """ The algorithm selects a task from queue and execute it on the machine

            Note:
                Task status and machine queue are updated here.
            Returns:
                the task id selected by the algorithm to be executed

        """

    @abstractmethod
    def terminate(self, task):
        """ the taks is terminated by this method

            Note:
                Tasks can be terminated by two ways: dropping from queue, or
                completing by the machine.
                the id of the completed task is added to the completed tasks
                queue of the machine while dropped tasks id is added to missed
                tasks queue of the machine. 

        """

    @abstractmethod
    def shutdown(self):
        """ shutdown the machine and change its status

            Note:
                it should also check the machine queue for further actions.

        """

    @abstractmethod
    def info(self):
        """ it gives the details about the machine

            Returns:
                a dictionary that includes: id, type, power, estimated available time
                content of queue, running task, number of completed task grouped by 
                task types and etc.

        """
