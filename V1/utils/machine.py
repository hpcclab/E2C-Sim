"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
import sys

from utils.base_machine import BaseMachine, MachineStatus
from utils.base_task import TaskStatus
from utils.task_type import UrgencyLevel
from utils.event import Event, EventTypes
from utils.queue import Queue
import utils.config as config
import time

from PyQt5.QtCore import  pyqtSignal


class Machine(BaseMachine):
    machine_signal = pyqtSignal(dict)
    timer = 0.1
    
    def __init__(self, id, replica_id, type, specs):
        super(Machine, self).__init__()
        self.id = id
        self.replica_id = replica_id
        self.type = type
        self.specs = specs
        self.status = MachineStatus.IDLE

        self.queue_size = config.machine_queue_size
        self.queue = Queue(maxsize = self.queue_size)
        self.running_task = []

        self.idle_time = config.time.gct()        

        self.completed_tasks = []
        self.xcompleted_tasks = []        
        self.missed = []
        
        self.stats = {'assigned_tasks': 0,
                      'completed_tasks': 0,
                      'xcompleted_tasks': 0,
                      'missed_BE_tasks': 0,
                      'missed_URG_tasks': 0,
                      'energy_usage': 0,
                      'wasted_energy': 0,
                      'idle_energy_usage':0}

        for task_type in config.task_types:
            self.stats[f'{task_type.name}-completed']=0
            self.stats[f'{task_type.name}-assigned']=0
            self.stats[f'{task_type.name}-wasted_energy']=0
            self.stats[f'{task_type.name}-energy_usage']=0
        
        self.sleep_time = 0.1

            
    
    def start(self):
        raise NotImplementedError
    
    def reset(self):       
        self.status = MachineStatus.IDLE
        self.queue = Queue(maxsize = self.queue_size)        
        self.running_task = []
        self.idle_time = config.time.gct()       

        self.completed_tasks = []
        self.xcompleted_tasks = []        
        self.missed = []  
       
        for key, _ in self.stats.items():
            self.stats[key] = 0

        
        
        
    def is_working(self):
        return bool(self.running_task)
    
    def select(self):
        if self.queue.empty():
            self.status = MachineStatus.IDLE
            return None
        else:
            task = self.queue.get()

            return task

    def provisional_map(self,task):
        
        if self.is_working():
            running_task = self.running_task[0]
            nxt_start_time = running_task.start_time + running_task.estimated_time[self.type.name] 
            if nxt_start_time > running_task.deadline:
                nxt_start_time = running_task.deadline 
        else:
            nxt_start_time = config.time.gct()
        
        if not self.queue.full():
            # self.queue.put(task)
            for t in self.queue.list:
                if nxt_start_time < t.deadline:
                    estimated_ct =nxt_start_time +  t.estimated_time[self.type.name]
                    nxt_start_time = estimated_ct if estimated_ct < t.deadline else t.deadline
                else:
                    estimated_ct = nxt_start_time
            self.queue.put(task)

            
            estimated_ct =nxt_start_time +  task.estimated_time[self.type.name]

            # if estimated_ct > task.deadline:
            #     estimated_ct = task.deadline
                   
            
            self.queue.remove(task)
        else:
            estimated_ct = float('inf')
        
        return estimated_ct


    def get_completion_time(self, task):
        start_time = self.idle_time if self.is_working() else config.time.gct()
        completion_time = start_time + task.execution_time[f'{self.type.name}-{self.replica_id}']
        completed = True

        if start_time > task.deadline:
            completion_time = start_time
            completed = False
        elif completion_time > task.deadline:
            completion_time = task.deadline
            completed = False            
        
        running_time = completion_time - start_time

        return completion_time, running_time, completed


    def admit(self, task):        
        if not self.queue.full():
            self.queue.put(task)            
            task.status = TaskStatus.PENDING                
            
            if config.gui==1:                
                self.machine_signal.emit({'type':'admitted',
                                        'time': config.time.gct(),
                                        'where':'machine: admit',
                                        'data':{'task':task,
                                                'assigned_machine':self,
                                             },
                                        
                                             })
                time.sleep(self.sleep_time)
            self.stats['assigned_tasks'] += 1
            self.stats[f'{task.type.name}-assigned'] += 1
            completion_time,running_time,_ = self.get_completion_time(task)
            self.idle_time = completion_time
            if not self.running_task:                
                task = self.select()
                self.execute(task)             
        elif self.queue.full() and self.queue.maxsize == 0 and not self.running_task:
            completion_time,running_time,_ = self.get_completion_time(task)
            self.idle_time = completion_time                         
            self.execute(task)                        
        else:
            return 'notEmpty', None 
        
        g = self.gain(task, completion_time)
        l = self.loss(task, running_time)
        return g, l
    

    def prune(self):
        for task in self.queue.list:
            if config.time.gct() > task.deadline :
                self.cancel(task)

    
    def execute(self, task):                 
        try:
            assert(not self.running_task), f'ERROR[machine.py -> execute()]: The machine {self.id} is already running a task'
        except  AssertionError as err:
            print(err)
            sys.exit()        
        self.running_task.append(task)
        if config.gui == 1:
            self.machine_signal.emit({  'type':'running',
                                        'where':'machine:execute',
                                        'time': config.time.gct(),
                                        'data':{'task':task,
                                                'assigned_machine':self,
                                             },
                                        
                                             })
            time.sleep(self.sleep_time)

        self.status = MachineStatus.WORKING
        task.status = TaskStatus.RUNNING        
        task.start_time = config.time.gct()
        task.completion_time = task.start_time + task.execution_time[f'{self.type.name}-{self.replica_id}']
        # rt: The time machine spent when it ran the task
        
        if task.urgency == UrgencyLevel.BESTEFFORT:

            if task.completion_time <= task.deadline:
                event_time = task.completion_time
                event_type = EventTypes.COMPLETION
                running_time = task.execution_time[f'{self.type.name}-{self.replica_id}']  

            elif task.start_time > task.deadline:
                task.missed_time = task.start_time
                running_time = 0.0
                task.completion_time = float('inf')
                event_time = task.missed_time
                event_type = EventTypes.DROPPED_RUNNING_TASK
            else:
                task.missed_time = task.deadline
                running_time = task.missed_time - task.start_time                
                task.completion_time = float('inf')
                event_time = task.missed_time
                event_type = EventTypes.DROPPED_RUNNING_TASK


        if task.urgency == UrgencyLevel.URGENT:
            if task.completion_time <= task.deadline - task.devaluation_window:
                event_time = task.completion_time
                event_type = EventTypes.COMPLETION
                running_time = task.execution_time[f'{self.type.name}-{self.replica_id}']  

            elif task.start_time > task.deadline - task.devaluation_window:
                task.missed_time = task.start_time
                running_time = 0.0
                task.completion_time = float('inf')
                event_time = task.missed_time
                event_type = EventTypes.DROPPED_RUNNING_TASK
            else:
                task.missed_time = task.deadline - task.devaluation_window
                running_time = task.missed_time - task.start_time                
                task.completion_time = float('inf')
                event_time = task.missed_time
                event_type = EventTypes.DROPPED_RUNNING_TASK
        
        
        event = Event(event_time, event_type, task)
        config.event_queue.add_event(event)
        
        s = '\n[ Task({}), Machine({}) ]: RUNNING        @time({:3.3f}) exec:{:3.3f} '.format(
            task.id, self.type.name,task.start_time, task.execution_time[f'{self.type.name}-{self.replica_id}'])
        self.machine_log = {"Task id":task.id,"Event Type":"RUNNING", "Time":event.time, "Execution time":task.execution_time[f'{self.type.name}-{self.replica_id}'],"Machine": self.id,"Type":'task'}
        config.log.write(s)
        
        # print(s)
        return running_time
    
    
    def gain(self, task, completion_time):
        delta = task.deadline
        if task.urgency == UrgencyLevel.BESTEFFORT:
            w = task.devaluation_window            
            
            if completion_time < delta-w:
                g = 2.5              
            elif completion_time >= delta-w and completion_time < delta:
                g = (2.5/w) * (delta  - completion_time)                
                #g = 1
            else:
                g = 0
            
        if task.urgency == UrgencyLevel.URGENT:
            if completion_time < delta:
                g = 100.0
            else:
                g = -100.0
        
        return g

    
    def loss(self, task, running_time):
        energy_consumption = running_time * self.specs['power']  # joule

        if task.urgency == UrgencyLevel.BESTEFFORT:
            alpha = 144* config.total_energy / config.available_energy            
            l =  alpha * energy_consumption / config.available_energy
                
        if task.urgency == UrgencyLevel.URGENT:
            beta = pow(2, -1* (config.available_energy / config.total_energy) )
            l = beta * energy_consumption / config.available_energy
        
        return l
    
    
                
    def drop(self):
        task = self.running_task.pop()               
        task.status = TaskStatus.MISSED        
        self.status = MachineStatus.IDLE

        if config.gui == 1:
            self.machine_signal.emit({  'type':'missed',
                                        'where':'machine:drop',
                                        'time': config.time.gct(),
                                        'data':{'task':task,
                                             'assigned_machine':self,
                                             },                                        
                                             })
            time.sleep(self.sleep_time)
                                             
        energy_consumption = (config.time.gct() - task.start_time) * self.specs['power'] 
        config.available_energy -= energy_consumption
        task.energy_usage = energy_consumption
        task.wasted_energy = energy_consumption

        if task.urgency == UrgencyLevel.BESTEFFORT:            
            self.stats['missed_BE_tasks'] += 1        
        elif task.urgency == UrgencyLevel.URGENT:            
            self.stats['missed_URG_tasks'] += 1
        self.stats['energy_usage'] += energy_consumption
        self.stats['wasted_energy'] += energy_consumption
        self.stats[f'{task.type.name}-energy_usage'] += energy_consumption
        self.stats[f'{task.type.name}-wasted_energy'] += energy_consumption

        if not self.queue.empty() :
            task = self.select()
            self.execute(task)

        s = '\n[ Task({:}), Machine({:}) ]: MISSED         @time({:3.3f})'.format(
            task.id, self.type.name, task.missed_time  ) 
        self.machine_log = {"Task id":task.id,"Event Type":"MISSED", "Time":task.missed_time, "Machine": self.id,"Type":'task'}

        config.log.write(s)       
        # print(s)
        return energy_consumption

    def cancel(self, task):
        
        task.status = TaskStatus.CANCELLED
        task.drop_time = config.time.gct()

        self.queue.remove(task)

        if config.gui==1:
            self.machine_signal.emit({'type':'cancelled_machine',
                            'time':config.time.gct(),
                            'where':'scheduelr: prune',
                            'data': {'task':task,
                                    'assigned_machine':self,                                                                                  
                                    },                                        
                                    })
            time.sleep(self.sleep_time)
        
        if self.running_task:
            if self.running_task[0].completion_time < self.running_task[0].deadline:
                nxt_start_time = self.running_task[0].completion_time
            else:
                nxt_start_time = self.running_task[0].missed_time
        else:
            nxt_start_time = config.time.gct()

        for task in self.queue.list:
            if nxt_start_time < task.deadline:
                completion_time = nxt_start_time + task.execution_time[f'{self.type.name}-{self.replica_id}']
                nxt_start_time = completion_time if completion_time < task.deadline else task.deadline
        self.idle_time = nxt_start_time

        if task.urgency == UrgencyLevel.BESTEFFORT:            
            self.stats['missed_BE_tasks'] += 1            
        
        if task.urgency == UrgencyLevel.URGENT:            
            self.stats['missed_URG_tasks'] += 1        
        
        
        s = '\n[ Task({:}), Machine({:}) ]: CANCELLED       @time({:3.3f})'.format(
            task.id, self.type.name, task.missed_time  )  
        self.machine_log = {"Task id":task.id,"Event Type":"CANCELLED", "Missed time":task.missed_time, "Machine": self.id,"Type":'task'}
        
        # print(s)
        config.log.write(s)    
        

    def terminate(self, task):
              
        self.running_task.pop()

        if config.gui == 1:
            self.machine_signal.emit({'type':'completion',
                                      'where':'machine:terminate',
                                      'time': config.time.gct(),
                                       'data':{'task':task,
                                             'assigned_machine':self,
                                             },
                                             })
            time.sleep(self.sleep_time)
        
        self.status = MachineStatus.IDLE        
        energy_consumption = task.execution_time[f'{self.type.name}-{self.replica_id}'] * self.specs['power'] 
        config.available_energy -= energy_consumption
        self.stats['energy_usage'] += energy_consumption
        self.stats[f'{task.type.name}-energy_usage'] += energy_consumption
        task.energy_usage = energy_consumption
        
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if task.completion_time <= task.deadline-task.devaluation_window:                
                task.status = TaskStatus.COMPLETED
               
                self.completed_tasks.append(task)
                self.stats['completed_tasks'] += 1
                self.stats[f'{task.type.name}-completed'] += 1                

            elif task.completion_time > task.deadline - task.devaluation_window and task.completion_time <= task.deadline :
                task.status = TaskStatus.XCOMPLETED                
                self.xcompleted_tasks.append(task)
                self.stats['xcompleted_tasks'] += 1
                self.stats[f'{task.type.name}-completed'] += 1
            
        if task.urgency == UrgencyLevel.URGENT:            
            task.status = TaskStatus.COMPLETED
            self.completed_tasks.append(task)
            self.stats['completed_tasks'] += 1
            self.stats[f'{task.type.name}-completed'] += 1
        s = '\n[ Task({:}), Machine({:}) ]: {:}      @time({:3.3f})'.format(
           task.id, self.type.name, task.status.name, task.completion_time )
        config.log.write(s)
        # print(s)

        if not self.queue.empty():
            task = self.select()            
            self.execute(task)  

        return energy_consumption

    def shutdown(self):
        self.status = MachineStatus.OFF

    def info(self):
       raise NotImplementedError
