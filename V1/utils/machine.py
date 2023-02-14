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
from utils.local_scheduler import LocalScheduler
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
        self.burst_time = 0


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

        self.local_scheduler = LocalScheduler(self)
        # print(self.local_scheduler.local_machine.id)

    
    def set_burst_time(self, value):
        self.burst_time = value

    def recreate_queue(self):
        self.queue = Queue(maxsize = self.queue_size)

            
    
    def start(self):
        raise NotImplementedError
    
    def reset_tt_stats(self):
        self.stats = {}

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
    # create new function that preempts

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
        task.start_time = start_time
        # remaining_time = task.remaining_time
        completion_time = start_time + float(task.remaining_time[f'{self.type.name}-{self.replica_id}'])
        completed = True
        if start_time > task.deadline:
            completion_time = start_time
            completed = False
        elif completion_time > task.deadline:
            completion_time = task.deadline
            completed = False            
        
        running_time = completion_time - start_time

        return completion_time, running_time, completed


    def prune(self):
        for task in self.queue.list:
            if config.time.gct() > task.deadline :
                self.local_scheduler.cancel(task)
   
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
        # time.sleep(self.sleep_time)
        # self.local_scheduler.preempt()
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

    def shutdown(self):
        self.status = MachineStatus.OFF

    def info(self):
       raise NotImplementedError
