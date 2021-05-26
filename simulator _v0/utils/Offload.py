"""
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

Machine class is used to create machines while each has a "machine_id"
and "machine_type". 
"start"/"shutdown" a machine are methods defined here to start using a
machine or shut it down.
A task is added to the machine queue, then start executing the task, and
finally completed using "add_task", "start_task", and "completing_task" 
methods.

"""

from Task import *
from EventQueue import *
from  Simulator import *
import Config


class Offload:
    
    simulator = Simulator()
    event_queue = EventQueue()
    
    def __init__(self, band_width,queue_length):
        
        self.queue_length = self.queue_length
        self.pending_queue = []
        self.completion_queue = []
        self.expected_available_time = 0.0 
        self.status = 'not_available'
        self.running_task=[];
        
    
    def start(self):
        # start offloading means that Cloud can accept tasks for processing.
        
        # assert that the offloading is not currently available. 
        assert self.status == 'not_available', "Offloading is currently "+ \
            str(self.status)
        # the status changed to available   
        self.status = 'available'
    
    
    def add_task(self, task):
        # It take a task and adds it to the pending_queue.
        # By adding a task to the pending_queue, its status changed to
        # "pending". 
        # The expected_available_time is also incremented by task
        # estimation of its execution time on this machine.
        # Finally, running_queue() is called to check if there is not
        # running_task, then the machine start executing current task.
        
        assert(self.status == 'available'), \
            "Task "+ str(task.task_id)+" cannot be offloaded while it is" \
                + self.status
                
        task.status = 'pending_offloaded'       
        self.pending_queue.append(task)
        self.expected_available_time += task.estimated_time['CLOUD']
        self.running_queue()
    
    def start_task(self, task):
        # It takes a task and start executing the task on the machine.
        # So, the status of task changed to "executing".
        # A completion_time of the task is calculated based on the real
        # execution time and a "completion" event is added to event_queue.
        
        task.status ='executing_offloaded'
        self.running_task.append(task)        
        task.completion_time = self.simulator.get_current_time() + \
            task.execution_time['CLOUD']
        event = Event(task.completion_time, 'completion_offloaded',
                      task)
        self.event_queue.add_event(event)
    
    
    def completing_task(self, task):
        # A completing_task is called whenever a "completion" event occurs.
        # It changed the status of "executing" task to "completed" and set
        # the completion time of the task. 
        # the task is also added to the completion_queue of the machine.
        
        
        task.status = 'completed_offloaded'
        self.completion_queue.append(task)
        self.running_task.remove(task)
        self.running_queue()        
        
    
    def running_queue(self):
        # It checks if the running_task is empty and there is a task in 
        # pending_queue, the task in head of pending_queue is popped and
        # is executed by the machine. 
        # If the machine is currently busy, the tasks in the pending_queue
        # should wait until completion the running_task.
        
        if(self.pending_queue):
           self.start_task(self.pending_queue.pop(0))
           
       
    
    def shutdown(self, shutdown_type='normal'):
        # "normal" shutdown changes the status of the machine to "shutdown"
        # but continue executing tasks have already assigned to the machine(
        # tasks in pending_queue or running_task)
        # "force" shutdown not only change the status of the machine to
        # "shutdown" but also drops all task in pending_queue or 
        # running_task.
        
        assert (self.status == 'not_available'), \
            "Warning: Cloud is currently "+ \
                str(self.status)
                
        if shutdown_type == 'force':
            
            if not self.running_task:
                for task in self.running_task:
                    print("Warning: There is an attempt to shutdown Cloud " +
                      " while task "+str(task.task_id)+
                      " is currently running on Cloud.")
                
                    task.status = 'dropped_offloaded'
                    task.drop_time = self.simulator.get_current_time()
                    self.running_task.remove(task)
        
            if not self.pending_queue:
                for task in self.pending_queue:
                    task.status = 'dropped_offloaded'
                    task.drop_time = self.simulator.get_current_time()
                    self.pending_queue.remove(task)
                    
        self.status = 'not_available'
    
    def query_info(self):
        pass