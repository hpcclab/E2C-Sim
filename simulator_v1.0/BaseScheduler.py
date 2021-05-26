from abc import ABCMeta,abstractmethod
import Config



class BaseScheduler:

    __metaclass__ = ABCMeta



    def __init__(self, machines_state):
        self._machines_state = machines_state
        self._batch_queue_size = Config.batch_queue_size
        self._batch_queue = [None]* self._batch_queue_size
    


    @abstractmethod
    def choose(self):
        """ Choose a task from batch queue for mapping decision

            returns:
                selected task object

        """

    @abstractmethod
    def offload(self, task):
        """ Offload the task to the cloud 
            
        """

    
    @abstractmethod
    def defer(self, task):
        """  defer the task for future mapping events

           

        """

    @abstractmethod
    def drop(self, task):
        """ drop a task 

            returns:
            1: dropped
            0: not dropped 

        """

    @abstractmethod
    def map(self, task):\
        """ map a task to a machine

            returns:
            (task, assigned_machine)

        """
    @abstractmethod
    def schedule(self, task):
        """
            It takes a task object and decide which actions should be taken
            as a scheduler.
            The action space is (drop, defer, offload, map).
            Each action is implemented separatedly, like map(self, task) and etc.
            The task is selected using choose(self) method.

            

        """



