from abc import ABCMeta, abstractmethod
import Config


class BaseScheduler:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = None
        self.batch_queue_size = Config.batch_queue_size
        self.batch_queue = [-1] * Config.batch_queue_size
        self.unlimited_queue = []
        self.unmapped_task = -1
        self.stats = {'mapped': [], 'dropped':[],
        'deferred':[], 'offloaded':[]}
        
    

    @abstractmethod
    def feed(self):
        """ It takes tasks from unlimited queue and fed them to
        the batch_queue
        it does nothing if there is no task in unlimited queue or
        returns a warning message if batch_queue is already full
        """

    @abstractmethod
    def choose(self):
        """ Choose a task from batch queue for mapping decision and 
         assgin it to the unmapped_task

            returns:
                index and value of selected task object 

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
    def map(self, task): \
        """ map a task to a machine

            returns:
            (task, assigned_machine)

        """


    @abstractmethod
    def select_machine(self, task): \
        """ Find a machine for a task to be assigned to

            returns:
            assigned_machine

        """


    @abstractmethod
    def schedule(self, task):
        """
            It takes a task object and decide which actions should be taken
            as a scheduler.
            The action space is (drop, defer, offload, map).
            Each action is implemented separately, like map(self, task) and etc.
            The task is selected using choose(self) method.

        """
