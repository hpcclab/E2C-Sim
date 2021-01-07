"""
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

Here, a Task class is defined to create tasks. All properties of a task
is defined here. To create a task, "task_id", "task_type_id", 
"estimated_time", "execution_time", and "arrival_time" should be given.
"start_time", "completion_time", and "drop_time" is initially set to "inf".
The initial status of task is also "arriving".

"""

class Task:
    # task_id: an integer assigned to a task.
    # task_type_id: An integer assigned to a task that determines its type
    # estimated_time: The estimation of the execution time of a task on
    # all machines. It should be a list.
    # execution_time: it is the real execution time of the task. it also
    # should be a list.
    # arrival_time: The time that task arrives to the system. 
    # start_time: The time a machine begin executing the task.
    # completion_time: The time that task is completed.
    # drop_time: If a task is dropped, drop_time indicated at what time
    # it has been dropped.
    # status: 'arriving'/'pending'/'executing'/'completed'/'dropped'
    
    def __init__(self, task_id, task_type_id, estimated_time,
                 execution_time, arrival_time):        
        self.task_id = task_id
        self.task_type_id = task_type_id
        self.estimated_time = estimated_time
        self.execution_time = execution_time
        self.arrival_time = arrival_time
        self.start_time = float('inf')
        self.completion_time = float('inf')
        self.drop_time = float('inf')
        self.status = 'arriving' 