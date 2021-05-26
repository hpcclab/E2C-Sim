from BaseTask import BaseTask


class Task(BaseTask):



    def __init__(self, id, type, est_exec_time,
                 execution_time, arrival_time, task_size=0.0):        
        self._id = id
        self._type = type
        self._est_exec_time = est_exec_time
        self.execution_time = execution_time
        self.arrival_time = arrival_time
        self.task_size = task_size
        self.start_time = float('inf')
        self.completion_time = float('inf')
        self.drop_time = float('inf')
        self.status = super().tasks_status['arriving']
        self.assigned_machine_id = None



    def info(self):
        """
            Returns:
            The details of the tasks as a dictionary of lists
        """

