from BaseTask import TaskStatus
from BaseScheduler import BaseScheduler
import Config



class RLS(BaseScheduler):
    
    machine_index = 0

    def __init__(self):
        super().__init__()
    


    def feed(self):

        while (self.unlimited_queue and (None in self.batch_queue)):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(None)
            self.batch_queue[empty_slot] = task


    def choose(self):
        index = 0
        print(self.batch_queue)
        if self.batch_queue[index] != None:
            task = self.batch_queue[index]
            self.batch_queue = self.batch_queue[:index] + self.batch_queue[index+1:]+[None]
            self.feed()
            self.unmapped_task = task
            return task
        else:
            print("No more task for scheduling ... \n")
            self.unmapped_task = None
            return None
        
        



    def offload(self, task):
        task.status = task.status_list['offloaded']

    
    def defer(self, task):
        if None in self.batch_queue:
            empty_slot = self.batch_queue.index(None)
            self.batch_queue[empty_slot] = task
        else:
            replaced_task = self.batch_queue[-1]
            self.unlimited_queue = [replaced_task] + self.unlimited_queue
            self.batch_queue[-1] = task
        task.status =  TaskStatus.DEFERRED


        


    def drop(self, task):
        task.status = TaskStatus.DROPPED
        task.drop_time = Config.current_time

    def map(self, task, machine):
        assignment = machine.admit(task)

        if  assignment:
            task.assigned_machine = machine
            print('Task '+ str(task.id) + " assigned to " +
            machine.type.name + " " + str(machine.id))
            return 1
        else: 
            self.defer(task)
            print("Task "+ str(task.id) +" is deferred")
            return 0
    
    



    def schedule(self):
        task = self.choose()

        if task != None:       
            assigned_machine = Config.machines[self.machine_index]
            self.map(task, assigned_machine )        
            if self.machine_index == len(Config.machines) -1 :
                self.machine_index = 0
            else:
                self.machine_index += 1 
            return assigned_machine
        else:
            return None


        

