"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus
from utils.base_scheduler import BaseScheduler
import utils.config as config

class FCFS(BaseScheduler):
    

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.name = 'FCFS'
        self.total_no_of_tasks = total_no_of_tasks
        self.prev_assignment_idx = -1
        self.gui_machine_log = []

    def choose(self, index=0):
        
        task = self.batch_queue.get(index)     
        self.unmapped_task.append(task)
        
        return task
    
    
    def defer(self, task):
        if config.time.gct() > task.deadline:
            self.drop(task)
            return 1
        self.unmapped_task.pop()
        task.status =  TaskStatus.DEFERRED
        task.no_of_deferring += 1
        self.batch_queue.put(task)
         
        self.stats['deferred'].append(task)
        s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
           task.id, config.time.gct())
        config.log.write(s)
        print(s)
        self.gui_machine_log.append({"Task id":task.id,"Event Type":"DEFERRED","Time":config.time.gct(), "Type":'task'})

    def drop(self, task):
        self.unmapped_task.pop()
        task.status = TaskStatus.CANCELLED
        task.drop_time = config.time.gct()
        self.stats['dropped'].append(task)        
        s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
            task.id, config.time.gct()       )
        config.log.write(s)
        print(s)
        self.gui_machine_log.append({"Task id":task.id,"Event Type":"DEFERRED","Time":config.time.gct(), "Type":'task'})

    def map(self, machine):
        task = self.unmapped_task.pop()
        assignment = machine.admit(task)
        if assignment != 'notEmpty':
            task.assigned_machine = machine
            self.stats['mapped'].append(task)
        else:
            self.defer(task)
    
    


    def schedule(self):
        self.gui_machine_log = []
        if self.batch_queue.empty():
            return 0
        self.choose()        
        machine_index = (self.prev_assignment_idx+1) % config.no_of_machines        
        machine = config.machines[machine_index]
        self.prev_assignment_idx = machine_index
        self.map(machine)
        return 1



    