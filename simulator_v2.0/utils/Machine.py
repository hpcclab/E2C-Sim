from random import gammavariate
from BaseMachine import BaseMachine, MachineStatus
from BaseTask import TaskStatus, UrgencyLevel
from Event import Event, EventTypes
import Config


class Machine(BaseMachine):
    
    def __init__(self, id, type, specs):
        self.id = id
        self.type = type
        self.specs = specs
        self.queue_size = Config.queue_size
        self.queue = [-1] * Config.queue_size
        self.completion_times = [-1] * (Config.queue_size+1)
        self.idle_time = Config.current_time        
        self.status = MachineStatus.IDLE
        self.available_time = Config.current_time 
        self.completed_tasks = []
        self.xcompleted_tasks = []
        self.running_task = [-1]
        self.missed = []
        self.stats = {'assigned_tasks': 0,
                      'completed_tasks': 0,
                      'xcompleted_tasks': 0,
                      'missed_BE_tasks': 0,
                      'missed_URG_tasks': 0,
                      'energy_usage': 0}

    def getType(self):
        return self.type.name

    def start(self):
        self.status = MachineStatus.IDLE
    
    def reset(self):
        self.queue = [-1] * Config.queue_size
        self.status = MachineStatus.IDLE
        self.available_time = Config.current_time 
        self.completion_times = [-1] * (Config.queue_size+1)
        self.completed_tasks = []
        self.xcompleted_tasks = []
        self.running_task = [-1]
        self.missed = []
        self.stats = {'assigned_tasks': 0,
                      'completed_tasks': 0,
                      'xcompleted_tasks': 0,
                      'missed_BE_tasks': 0,
                      'missed_URG_tasks': 0,
                      'energy_usage': 0}


    def select(self):
        if self.queue[0] != -1 :
            index = 0
            return index
        else:
            self.status = MachineStatus.IDLE
            return -1

    def execute(self, task):        
        task.status = TaskStatus.RUNNING
        self.status = MachineStatus.WORKING
        task.start_time = Config.current_time
        self.running_task[0] = task
        task.completion_time = task.start_time + task.execution_time[self.type.name]
        
        if task.urgency == UrgencyLevel.BESTEFFORT:           
                
            if task.completion_time <= (task.deadline + task.devaluation_window):
                event_time = task.completion_time
                event_type = EventTypes.COMPLETION
                rt = task.execution_time[self.type.name]
            else:
                if task.start_time > task.deadline + task.devaluation_window:
                    task.missed_time = task.start_time
                else:
                    task.missed_time = task.deadline + task.devaluation_window

                rt = task.missed_time - task.start_time                
                task.completion_time = float('inf')
                event_time = task.missed_time
                event_type = EventTypes.DROPPED_RUNNING_TASK
                
               
        if task.urgency == UrgencyLevel.URGENT:

            if task.completion_time <= task.deadline:
                event_time = task.completion_time               
                event_type = EventTypes.COMPLETION
                rt = task.execution_time[self.type.name]
            else:
                if task.start_time > task.deadline :
                    task.missed_time = task.start_time
                else:
                    task.missed_time = task.deadline 

                rt = task.missed_time - task.start_time  
                task.completion_time = float('inf')
                event_time = task.missed_time
                event_type = EventTypes.DROPPED_RUNNING_TASK
        
        self.idle_time = event_time

        event = Event(event_time, event_type, task)
        Config.event_queue.add_event(event)
        self.completion_times[0] = event_time
        s = '\n[ Task({}), Machine({}) ]: RUNNING        @time({:3.3f}) exec:{:3.3f}'.format(
            task.id, self.id,task.start_time, task.execution_time[self.type.name])
        Config.log.write(s)
        #print(s)
        return rt
    
    def get_available_time (self, slot_num):

        if self.queue_size >0:
            for i in range(slot_num+1):
                task = self.queue[i]
                #starting_time = self.completion_times[slot_num]
                starting_time = self.completion_times[i]
                ct = starting_time + task.execution_time[self.type.name]
                delta = task.deadline

                if task.urgency == UrgencyLevel.BESTEFFORT:
                    if ct > delta + task.devaluation_window:
                        ct = delta + task.devaluation_window
                        
                        
                if task.urgency == UrgencyLevel.URGENT:
                    if ct > delta:
                        ct = delta
                self.completion_times[i+1] = ct
                rt = ct - starting_time
        else:
            pass


        return rt, ct
    
    def gain(self, task, completion_time):
        delta = task.deadline
        if task.urgency == UrgencyLevel.BESTEFFORT:
            w = task.devaluation_window
            
            
            if completion_time < delta:
                g = 5
            elif completion_time >= delta and completion_time < delta + w:
                g = (1.0/w) * (delta  + w - completion_time)
            else:
                g = -5
            
        if task.urgency == UrgencyLevel.URGENT:
            if completion_time < delta:
                g = 100.0
            else:
                g = -100.0
        
        return g

    
    def loss(self, task, running_time):
        energy_consumption = running_time * self.specs['power'] / 3600 # watt.hour

        if task.urgency == UrgencyLevel.BESTEFFORT:
            alpha = Config.total_energy / Config.available_energy            
            l = alpha * energy_consumption / Config.available_energy
                
        if task.urgency == UrgencyLevel.URGENT:
            beta = pow(2, -1* (Config.available_energy / Config.total_energy) )
            l = beta * energy_consumption / Config.available_energy
        
        return l
    
    
                
    def drop(self):
        task = self.running_task[0]        
        self.running_task[0] = -1
        self.completion_times[0] = -1
        task.status = TaskStatus.MISSED
        
        energy_consumption = (task.missed_time - task.start_time) * self.specs['power'] / 3600 # watt.hour
        if task.urgency == UrgencyLevel.BESTEFFORT:            
            self.stats['missed_BE_tasks'] += 1
        
        if task.urgency == UrgencyLevel.URGENT:            
            self.stats['missed_URG_tasks'] += 1
        
        self.status = MachineStatus.IDLE
        Config.available_energy -= energy_consumption
        self.stats['energy_usage'] += energy_consumption
        s = '\n[ Task({:}), Machine({:}) ]: MISSED         @time({:3.3f})'.format(
            task.id, self.id, task.missed_time  )
        Config.log.write(s)
        #print(s)

        if self.queue_size>0:
            index = self.select()
            if index != -1:
                task = self.queue[index]
                self.queue = self.queue[:index] + self.queue[index + 1:] + [-1]
                self.execute(task)
        return energy_consumption


    def terminate(self, task):
        #task = self.running_task[0]        
        self.running_task[0] = -1
        self.completion_times[0] = -1
        self.status = MachineStatus.IDLE        
        energy_consumption = task.execution_time[self.type.name] * self.specs['power'] / 3600 # watt.hour
        Config.available_energy -= energy_consumption
        self.stats['energy_usage'] += energy_consumption

        if task.urgency == UrgencyLevel.BESTEFFORT:
            if task.completion_time <= task.deadline:
                task.status = TaskStatus.COMPLETED
                self.completed_tasks.append(task)
                self.stats['completed_tasks'] += 1

            elif task.completion_time > task.deadline and task.completion_time <= task.deadline + task.devaluation_window:
                task.status = TaskStatus.XCOMPLETED
                self.xcompleted_tasks.append(task)
                self.stats['xcompleted_tasks'] += 1
            
        if task.urgency == UrgencyLevel.URGENT:            
            task.status = TaskStatus.COMPLETED
            self.completed_tasks.append(task)
            self.stats['completed_tasks'] += 1
        s = '\n[ Task({:}), Machine({:}) ]: {:}      @time({:3.3f})'.format(
           task.id, self.id, task.status.name, task.completion_time )
        Config.log.write(s)
        #print(s)

        if self.queue_size>0:
            index = self.select()
            if index != -1:
                task = self.queue[index]
                self.queue = self.queue[:index] + self.queue[index + 1:] + [-1]
                self.execute(task)  
        

        return energy_consumption 
        

    def admit(self, task):
        if self.queue_size>0:
            if -1 in self.queue:
                empty_slot = self.queue.index(-1)
                self.queue[empty_slot] = task
                task.status = TaskStatus.PENDING                
                self.stats['assigned_tasks'] += 1
                
                                
                if -1 in self.running_task:
                    index = self.select()                    
                    task = self.queue[index]
                    self.queue = self.queue[:index] + self.queue[index + 1:] + [-1]
                    running_time = self.execute(task)
                    self.available_time = self.running_task[0].completion_time                    
                else:                    
                    running_time, self.available_time = self.get_available_time(empty_slot)
                g = self.gain(task, self.available_time)
                l = self.loss(task, running_time)
                
                #return g-l  # excluded when energy is not important
                return g
            
            else:                
                return 'notEmpty'
            
        else:
            if -1 in self.running_task:
                running_time = self.execute(task)
                self.available_time = self.running_task[0].completion_time
                g = self.gain(task, self.available_time)
                l = self.loss(task, running_time)
                #print ('machine {} task:{} g-l: {}'.format(self.type.name, task.id, g-l))
                #return g-l # excluded when energy is not important
                return g
            else:                
                return 'notEmpty'
    
    def provisional_map(self,task):
        if -1 in self.running_task:
            ct = Config.current_time + task.execution_time[self.type.name]
            #print('AT: {} Machine {} '.format(ct, self.id))
            return ct
        
        elif -1 in self.queue:            
            empty_slot = self.queue.index(-1)  
            self.queue[empty_slot] = task
            _, ct = self.get_available_time(empty_slot)
            #print('AT: {} Machine {} '.format(ct, self.id))
            self.queue[empty_slot] = -1
            return ct   
        else:
            return float('inf')
        
        



    def shutdown(self):

        self.status = MachineStatus.OFF

    def info(self):
        # Incomplete as of now
        completed = ""

        dictionary = ("ID: " + self.id + ", Type: " + self.type +
                      ", Status: " + self.status)
        print(dictionary)
        return dictionary
