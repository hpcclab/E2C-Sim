from BaseScheduler import BaseScheduler
import Config


class FCFS(BaseScheduler):
    
    machine_index = 0

    def __init__(self, machines_state):
        super().__init__()
    


    def feed(self):

        while (self.unlimited_queue and (None in self.batch_queue)):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(None)
            self.batch_queue[empty_slot] = task


    def choose(self):
        index = 0
        if self.batch_queue[index] != None:
            task = self.batch_queue[0]
        else:
            print("No more task for scheduling ... \n")
        
        self.batch_queue = self.batch_queue[:index] + self.batch_queue[index+1:]+[None]
        self.feed()

        return index, task



    def offload(self, task):
        task.status = task.status_list['offloaded']

    
    def defer(self, task):
        replaced_task = self.batch_queue[-1]
        self.unlimited_queue = [replaced_task] + self.unlimited_queue
        self.batch_queue[-1] = task
        task.status =  task.status_list['deferred']


        


    def drop(self, task):
        task.status = task.status_list['dropped']
        task.drop_time = Config.current_time

    def map(self, task, machine):
        if (None in machine._queue):
            empty_slot = machine._queue.index(None)
            machine._queue[empty_slot] = task
            task.status = task.status_list['pending']
            return 1
        else:
            print("Warning: Task "+ task._id +" mapped to machine " + 
            machine._id + " that has no empty slot\n")
            self.defer(self, task)
            print("Task "+ task._id +" is deferred")
            return 0
    



    def schedule(self):
        _ , task = self.choose(self)
        self.map(self,task, Config.machines[self.machine_index] )
        if self.machine_index == len(Config.machines) -1 :
            self.machine_index = 0
        else:
            self.machine_index += 1 


        

