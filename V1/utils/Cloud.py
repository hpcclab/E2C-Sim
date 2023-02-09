"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus, UrgencyLevel
from utils.event import Event, EventTypes
import utils.config as config
from math import ceil


class Cloud:
    
    def __init__(self, bandwidth, latency):
        self.bandwidth = config.bandwidth
        self.latency = config.network_latency
        self.completed_tasks = []
        self.xcompleted_tasks = []
        self.missed_tasks = []
        self.stats = {'offloaded_tasks': 0,
                      'completed_tasks': 0,
                      'xcompleted_tasks': 0,
                      'missed_BE_tasks': 0,
                      'missed_URG_tasks': 0
                      }
    
    def reset(self):
        self.completed_tasks = []
        self.xcompleted_tasks = []
        self.missed_tasks = []
        self.stats = {'offloaded_tasks': 0,
                      'completed_tasks': 0,
                      'xcompleted_tasks': 0,
                      'missed_BE_tasks': 0,
                      'missed_URG_tasks': 0
                      }


    def admit(self, task):
        task.status = TaskStatus.OFFLOADED
        self.stats['offloaded_tasks'] += 1
        task.start_time = config.time.gct()
        no_of_packets = ceil(task.task_size / config.bandwidth)       
        task.completion_time = task.start_time + no_of_packets * config.latency + task.execution_time['CLOUD']        
        
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if task.completion_time <= task.deadline + task.devaluation_window:
                reward = 0.1         
            else:
                reward = -0.5
            
            
        elif task.urgency == UrgencyLevel.URGENT:
            if task.completion_time <= task.deadline:
                reward = 0.5
            else:
                reward = -0.5
           
            
        event_time = task.completion_time
        event_type = EventTypes.OFFLOADED     
        event = Event(event_time, event_type, task)
        config.event_queue.add_event(event)

        s = '\n[ Task({}), ____ ]: OFFLOADED        @time({:3.3f}) exec+net:{:3.3f}'.format(
            task.id, task.start_time, no_of_packets * config.latency + task.execution_time['CLOUD'])
        
        #print(s)

        return reward
    
    def terminate(self, task):
        
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if task.completion_time <= task.deadline:
                task.status = TaskStatus.COMPLETED
                self.completed_tasks.append(task)
                self.stats['completed_tasks'] += 1

            elif task.completion_time > task.deadline and task.completion_time <= task.deadline + task.devaluation_window:
                task.status = TaskStatus.XCOMPLETED
                self.xcompleted_tasks.append(task)
                self.stats['xcompleted_tasks'] += 1
            
            else:
                task.status = TaskStatus.MISSED
                self.missed_tasks.append(task)
                self.stats['missed_BE_tasks'] += 1
            
        if task.urgency == UrgencyLevel.URGENT:
            if task.completion_time <= task.deadline:            
                task.status = TaskStatus.COMPLETED
                self.completed_tasks.append(task)
                self.stats['completed_tasks'] += 1
            else:
                task.status = TaskStatus.MISSED
                self.missed_tasks.append(task)
                self.stats['missed_URG_tasks'] += 1
        
        s = '\n[ Task({}), ____ ]: {}        @time({:3.3f}) on CLOUD'.format(
            task.id, task.status, task.completion_time)        
        #print(s)
        