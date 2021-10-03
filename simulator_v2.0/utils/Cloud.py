from BaseTask import TaskStatus, UrgencyLevel
from Event import Event, EventTypes
import Config
from math import ceil


class Cloud:
    
    def __init__(self, bandwidth, latency):
        self.bandwidth = Config.bandwidth
        self.latency = Config.latency
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
        task.start_time = Config.current_time
        no_of_packets = ceil(task.task_size / Config.bandwidth)       
        task.completion_time = task.start_time + no_of_packets * Config.latency + task.execution_time['CLOUD']        
        
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
        Config.event_queue.add_event(event)

        s = '\n[ Task({}), ____ ]: OFFLOADED        @time({:3.3f}) exec+net:{:3.3f}'.format(
            task.id, task.start_time, no_of_packets * Config.latency + task.execution_time['CLOUD'])
        Config.log.write(s)
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
        Config.log.write(s)
        #print(s)
        