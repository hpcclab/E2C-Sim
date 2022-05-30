"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus
from utils.base_scheduler import BaseScheduler
import utils.config as config
from utils.event import Event, EventTypes


class MM(BaseScheduler):
    

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.name = 'MM'
        self.total_no_of_tasks = total_no_of_tasks
        self.gui_machine_log = []


    def choose(self, index=0):
        task = self.batch_queue.get(index)     
        self.unmapped_task.append(task)
        if config.settings['verbosity']:
            s =f'\n{task.id} selected --> BQ = '
            bq = [t.id for t in self.batch_queue.list]
            s += f'{bq}'
            s += f'\nexecutime: {task.execution_time}'
            s += f'\testimeated_time{task.estimated_time}'

            config.log.write(s)
        
        return task
    
    
    def defer(self, task):
        if config.time.gct() > task.deadline:
            self.drop(task)
            return 1
        self.unmapped_task.pop()
        task.status =  TaskStatus.DEFERRED
        task.no_of_deferring += 1
        self.batch_queue.put(task)

        event_time = config.event_queue.event_list[0].time
        event_type = EventTypes.DEFERRED
        event = Event(event_time, event_type, task)
        config.event_queue.add_event(event)
         
        self.stats['deferred'].append(task)
        if config.settings['verbosity']:
            s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
            task.id, config.time.gct())
            config.log.write(s)
        self.gui_machine_log.append({"Task id":task.id,"Event Type":"DEFERRED","Time":config.time.gct(), "Type":'task'})

    def drop(self, task):
        self.unmapped_task.pop()
        task.status = TaskStatus.CANCELLED
        task.drop_time = config.time.gct()
        self.stats['dropped'].append(task) 
        if config.settings['verbosity']:       
            s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
                task.id, config.time.gct()       )
            config.log.write(s)
        self.gui_machine_log.append({"Task id":task.id,"Event Type":"CANCELLED","Time":config.time.gct(), "Type":'task'})

    def map(self, machine):
        task = self.unmapped_task.pop()
        assignment = machine.admit(task)
        if assignment != 'notEmpty':
            task.assigned_machine = machine
            self.stats['mapped'].append(task)
        else:
            self.defer(task)
    
    def prune(self):

        for task in self.batch_queue.list:
            if config.time.gct() > task.deadline:                
                task.status = TaskStatus.CANCELLED
                task.drop_time = config.time.gct()
                self.stats['dropped'].append(task) 
                self.batch_queue.remove(task)


    
    def phase1(self):
       
        provisional_map = []
        index = 0 
        # s = '\nPHASE-I:'        
        self.prune()       
        for task in self.batch_queue.list:
            min_ct = float('inf')
            min_ct_machine = None            
            for machine in config.machines:
                pct = machine.provisional_map(task)
                # s += f'\ntask: {task.id} on {machine.type.name} --> pct: {pct}'                
                if pct < min_ct:
                    min_ct = pct
                    min_ct_machine = machine 
           
        
            provisional_map.append([task, min_ct, min_ct_machine, index])
            index += 1 
             
        #config.log.write(s)
        
        return provisional_map
    

    def phase2(self, provisional_map):
        provisional_map_machines = []        
        for machine in config.machines:
            if not machine.queue.full():
                min_ct =float('inf')
                task = None
                index = None
                for pair in provisional_map:                    
                    if pair[2] != None and pair[2].id == machine.id and pair[1] < min_ct:
                        task = pair[0]
                        min_ct = pair[1]
                        index = pair[3]   
                provisional_map_machines.append([task,machine,index])

        return provisional_map_machines



    def schedule(self):
        self.gui_machine_log = []

        if config.settings['verbosity']:
            s = f'\n Current State @{config.time.gct()}'
            s = '\nBQ = '
            bq = [t.id for t in self.batch_queue.list]
            s += f'{bq}'
            s += '\n\nMACHINES ==>>>'
            for m in config.machines:
                s += f'\n\tMachine {m.type.name} :'
                if m.running_task:
                    r = [m.running_task[0].id]
                else:
                    r = []
                mq = [t.id for t in m.queue.list]
                r.append(mq)
                s +=f'\t{r}'
            config.log.write(s)
        
        provisional_map = self.phase1()
        provisional_map_machines = self.phase2(provisional_map)

        for pair in provisional_map_machines:
            task = pair[0]
            assigned_machine = pair[1]  

            if task != None :
                index = self.batch_queue.list.index(task)                                               
                task = self.choose(index)
                self.map(assigned_machine)
                s = f"\ntask:{task.id}  assigned to:{assigned_machine.type.name}  ec:{pair[2]}   delta:{task.deadline}"
                config.log.write(s)
                return assigned_machine
        return None
    #####
    