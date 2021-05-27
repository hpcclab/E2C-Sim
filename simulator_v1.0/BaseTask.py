from abc import ABCMeta,abstractmethod


class BaseTask:

    __metaClass__ = ABCMeta

    tasks_status = ['arriving' , 'offloaded', 'pending', 'executing', 'completed','dropped']

    def __init__(self):
        pass
        


    @abstractmethod
    def info(self):
        """ it gives the details about the task

            Returns:
                a dictionary that includes: id, type, status, assigned machine if
                it is mapped, etc.

        """