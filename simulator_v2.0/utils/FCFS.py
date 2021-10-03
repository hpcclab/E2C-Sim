from BaseTask import TaskStatus, UrgencyLevel
from BaseScheduler import BaseScheduler
import Config


class FCFS(BaseScheduler):
    machine_index = 0

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.total_no_of_tasks = total_no_of_tasks

    def feed(self):

        while self.unlimited_queue and (-1 in self.batch_queue):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task

    def choose(self):
        index = 0        
        if self.batch_queue[index] != -1:
            self.unmapped_task = self.batch_queue[index]
            self.batch_queue = self.batch_queue[:index] + self.batch_queue[index+1:]+[-1]            
            self.feed()
            return self.unmapped_task
                         
        else:            
            self.unmapped_task = -1
            return -1

    def offload(self, task):
        task.status = task.status_list['offloaded']

    def defer(self, task):
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if Config.current_time > task.deadline + task.devaluation_window:
                self.drop(task)
                return
        elif task.urgency == UrgencyLevel.URGENT:
            if Config.current_time > task.deadline:
                self.drop(task)
                return
        
        if -1 in self.batch_queue:
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task
        else:
            replaced_task = self.batch_queue[-1]
            self.unlimited_queue = [replaced_task] + self.unlimited_queue
            self.batch_queue[-1] = task
        task.status =  TaskStatus.DEFERRED
        self.stats['deferred'].append(task)
        s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
           task.id, Config.current_time        )
        Config.log.write(s)
        print(s)

    def drop(self, task):
        task.status = TaskStatus.CANCELLED
        task.drop_time = Config.current_time
        self.stats['dropped'].append(task)        
        s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
            task.id, Config.current_time        )
        Config.log.write(s)

    def map(self, machine):
        assignment = machine.admit(self.unmapped_task)

        if assignment != 'notEmpty':
            self.unmapped_task.assigned_machine = machine
            self.stats['mapped'].append(self.unmapped_task)
        else:
            self.defer(self.unmapped_task)
        

    def schedule(self):
        
        if self.choose() == -1 :
            return -1
            
        assigned_machine = Config.machines[self.machine_index]
        self.map(assigned_machine)
        if self.machine_index == len(Config.machines) - 1:
            self.machine_index = 0
        else:
            self.machine_index += 1
    
