
from utils.base_machine import BaseMachine, MachineStatus
from utils.base_task import TaskStatus
from utils.task_type import UrgencyLevel
import utils.config as config
import time

# Control policies and the machine chooses the type of scheduler
class LocalScheduler():
# work in progress
    def __init__(self, machine):
        self.local_machine = machine
        self.id = machine.id
        # self.burst_time = burst_time
      
    # Preempt a task (pause it and put it back onto queue)
    def preempt(self):
        preempted_task = self.local_machine.running_task.pop()
        preempted_task.status = TaskStatus.PREEMPTED
        self.local_machine.status = MachineStatus.IDLE

        if config.gui==1:                
                self.local_machine.machine_signal.emit({'type':'preempted',
                                        'time': config.time.gct(),
                                        'where':'machine: drop',
                                        'data':{'task':preempted_task,
                                                'assigned_machine':self.local_machine,
                                             },
                                        
                                             })
                time.sleep(self.local_machine.sleep_time)

        # Calculate the current time 
        current_time = config.time.gct()
        preempted_task.drop_time = config.time.gct()
        # Find the time spent running by subtracting the starting time from the current time.
        remaining_time = preempted_task.remaining_time[f'{self.local_machine.type.name}-{self.local_machine.replica_id}'] - (current_time - preempted_task.start_time)
        if remaining_time <= 0:
            remaining_time = 0 
        s = '\n[ Task({:}), Machine({:}) ]: PREEMPTED         @time({:3.3f} | REMAINING: {:3.3f})'.format(
            preempted_task.id, self.local_machine.type.name, config.time.gct(), remaining_time   ) 
        print(s)
        preempted_task.remaining_time[f'{self.local_machine.type.name}-{self.local_machine.replica_id}'] = remaining_time
        #self.local_machine.queue.put(preempted_task)
        self.admit(preempted_task)

    # Assign (admit) a new task from the queue to the machine
    def admit(self, task):
        #print(self.queue.maxsize)       
        if not self.local_machine.queue.full():
            # Add task to queue and set to pending
            self.local_machine.queue.put(task)            
            task.status = TaskStatus.PENDING                
            
            if config.gui==1:                
                self.local_machine.machine_signal.emit({'type':'admitted',
                                        'time': config.time.gct(),
                                        'where':'machine: admit',
                                        'data':{'task':task,
                                                'assigned_machine':self.local_machine,
                                             },
                                        
                                             })
                time.sleep(self.local_machine.sleep_time)
            # Increment assigned tasks and find the completion (when it will be finished) and running (# of secs to complete) time of tasks.
            self.local_machine.stats['assigned_tasks'] += 1
            self.local_machine.stats[f'{task.type.name}-assigned'] += 1
            completion_time,running_time,_ = self.local_machine.get_completion_time(task)
            
            # Will be idle at completion time
            self.local_machine.idle_time = completion_time
            # If a task is not currently running, then select a task and execute it.
            if not self.local_machine.running_task:                
                task = self.select()
                self.local_machine.execute(task)         
        # If the queue is full and the max queue size is 0 and no task is currently running
        # execute the task (no need to select)         
        elif self.local_machine.queue.full() and self.local_machine.queue.maxsize == 0 and not self.local_machine.running_task:
            completion_time,running_time,_ = self.local_machine.get_completion_time(task)
            self.local_machine.idle_time = completion_time                         
            self.local_machine.execute(task)                        
        else:
            return 'notEmpty', None 

        g = self.local_machine.gain(task, completion_time)
        l = self.local_machine.loss(task, running_time)
        return g, l
        #print(self.queue)

    # Choose which task from the queue
    def select(self):
        if self.local_machine.queue.empty():
            self.local_machine.status = MachineStatus.IDLE
            return None
        else:
            task = self.local_machine.queue.get()
            return task

    # Drop the currently running task
    def drop(self):
        task = self.local_machine.running_task.pop()               
        task.status = TaskStatus.MISSED        
        self.local_machine.status = MachineStatus.IDLE

        if config.gui == 1:
            self.local_machine.machine_signal.emit({  'type':'missed',
                                        'where':'machine:drop',
                                        'time': config.time.gct(),
                                        'data':{'task':task,
                                             'assigned_machine':self.local_machine,
                                             },                                        
                                             })
            time.sleep(self.local_machine.sleep_time)
                                             
        energy_consumption = (config.time.gct() - task.start_time) * self.local_machine.specs['power'] 
        config.available_energy -= energy_consumption
        task.energy_usage = energy_consumption
        task.wasted_energy = energy_consumption

        if task.urgency == UrgencyLevel.BESTEFFORT:            
            self.local_machine.stats['missed_BE_tasks'] += 1        
        elif task.urgency == UrgencyLevel.URGENT:            
            self.local_machine.stats['missed_URG_tasks'] += 1
        self.local_machine.stats['energy_usage'] += energy_consumption
        self.local_machine.stats['wasted_energy'] += energy_consumption
        self.local_machine.stats[f'{task.type.name}-energy_usage'] += energy_consumption
        self.local_machine.stats[f'{task.type.name}-wasted_energy'] += energy_consumption

        if not self.local_machine.queue.empty() :
            task = self.select()
            self.local_machine.execute(task)

        s = '\n[ Task({:}), Machine({:}) ]: MISSED         @time({:3.3f})'.format(
            task.id, self.local_machine.type.name, task.missed_time  ) 
        self.local_machine.machine_log = {"Task id":task.id,"Event Type":"MISSED", "Time":task.missed_time, "Machine": self.id,"Type":'task'}

        config.log.write(s)       
        # print(s)
        return energy_consumption

    def terminate(self, task):
        self.local_machine.running_task.pop()

        if config.gui == 1:
            self.local_machine.machine_signal.emit({'type':'completion',
                                      'where':'machine:terminate',
                                      'time': config.time.gct(),
                                       'data':{'task':task,
                                             'assigned_machine':self.local_machine,
                                             },
                                             })
            time.sleep(self.local_machine.sleep_time)
        
        self.local_machine.status = MachineStatus.IDLE        
        energy_consumption = task.execution_time[f'{self.local_machine.type.name}-{self.local_machine.replica_id}'] * self.local_machine.specs['power'] 
        config.available_energy -= energy_consumption
        self.local_machine.stats['energy_usage'] += energy_consumption
        self.local_machine.stats[f'{task.type.name}-energy_usage'] += energy_consumption
        task.energy_usage = energy_consumption
        
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if task.completion_time <= task.deadline-task.devaluation_window:                
                task.status = TaskStatus.COMPLETED
               
                self.local_machine.completed_tasks.append(task)
                self.local_machine.stats['completed_tasks'] += 1
                self.local_machine.stats[f'{task.type.name}-completed'] += 1                

            elif task.completion_time > task.deadline - task.devaluation_window and task.completion_time <= task.deadline :
                task.status = TaskStatus.XCOMPLETED                
                self.local_machine.xcompleted_tasks.append(task)
                self.local_machine.stats['xcompleted_tasks'] += 1
                self.local_machine.stats[f'{task.type.name}-completed'] += 1
            
        if task.urgency == UrgencyLevel.URGENT:            
            task.status = TaskStatus.COMPLETED
            self.local_machine.completed_tasks.append(task)
            self.local_machine.stats['completed_tasks'] += 1
            self.local_machine.stats[f'{task.type.name}-completed'] += 1
        s = '\n[ Task({:}), Machine({:}) ]: {:}      @time({:3.3f})'.format(
           task.id, self.local_machine.type.name, task.status.name, task.completion_time )
        config.log.write(s)
        # print(s)

        if not self.local_machine.queue.empty():
            task = self.select()            
            self.local_machine.execute(task)  

        return energy_consumption

    def cancel(self, task):
        task.status = TaskStatus.CANCELLED
        task.drop_time = config.time.gct()

        self.local_machine.queue.remove(task)

        if config.gui==1:
            self.local_machine.machine_signal.emit({'type':'cancelled_machine',
                            'time':config.time.gct(),
                            'where':'scheduelr: prune',
                            'data': {'task':task,
                                    'assigned_machine':self.local_machine,                                                                                  
                                    },                                        
                                    })
            time.sleep(self.local_machine.sleep_time)
        
        if self.local_machine.running_task:
            if self.local_machine.running_task[0].completion_time < self.local_machine.running_task[0].deadline:
                nxt_start_time = self.local_machine.running_task[0].completion_time
            else:
                nxt_start_time = self.local_machine.running_task[0].missed_time
        else:
            nxt_start_time = config.time.gct()

        for task in self.local_machine.queue.list:
            if nxt_start_time < task.deadline:
                completion_time = nxt_start_time + task.execution_time[f'{self.local_machine.type.name}-{self.local_machine.replica_id}']
                nxt_start_time = completion_time if completion_time < task.deadline else task.deadline
        self.local_machine.idle_time = nxt_start_time

        if task.urgency == UrgencyLevel.BESTEFFORT:            
            self.local_machine.stats['missed_BE_tasks'] += 1            
        
        if task.urgency == UrgencyLevel.URGENT:            
            self.local_machine.stats['missed_URG_tasks'] += 1        
        
        
        s = '\n[ Task({:}), Machine({:}) ]: CANCELLED       @time({:3.3f})'.format(
            task.id, self.local_machine.type.name, task.missed_time  )  
        self.local_machine.machine_log = {"Task id":task.id,"Event Type":"CANCELLED", "Missed time":task.missed_time, "Machine": self.id,"Type":'task'}
        
        # print(s)
        config.log.write(s)