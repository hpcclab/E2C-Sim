"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
from BaseTask import BaseTask, TaskStatus, UrgencyLevel


class Task(BaseTask):

    def __init__(self, id, type, task_size,est_exec_time,
                 execution_time, arrival_time):
        self.id = id
        self.type = type
        self.urgency = type.urgency
        self.deadline = arrival_time + type.deadline
        self.devaluation_window = 0.5 * type.deadline
        self.estimated_time = est_exec_time
        self.execution_time = execution_time
        self.arrival_time = arrival_time
        self.task_size = task_size
        self.start_time = float('inf')
        self.completion_time = float('inf')
        self.missed_time = float('inf')
        self.drop_time = float('inf')
        self.status = TaskStatus.ARRIVING
        self.assigned_machine = None
        self.no_of_deferring = 0

    def info(self):
        d = {
            'id': self.id,
            'type': self.type,
            'status': self.status,
            'urgency': self.urgency,
            'deadline':self.deadline,
            'extended_deadline':self.deadline + self.devaluation_window,
            'estimated_time':self.est_exec_time,
            'execution_time': self.execution_time,
            'arrival_time':self.arrival_time,
            'start_time': self.start_time,
            'completion_time':self.completion_time,
            'assigned_to':self.assigned_machine            
        }
        """
            Returns:
            The details of the tasks as a dictionary of lists

        """

        return d
