"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
import numpy as np

from utils.base_task import TaskStatus
from utils.base_scheduler import BaseScheduler
import utils.config as config
import time

class FEE(BaseScheduler):
    
    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.name = 'FEE'
        self.total_no_of_tasks = total_no_of_tasks
        self.priority_queue = []
        self.sleep_time = 0.1
            
    def choose(self, index=0):
        task = self.batch_queue.get(index)     
        self.unmapped_task.append(task)
        if config.gui==1:
            self.decision.emit({'type':'choose',
                                'time':config.time.gct(),
                                'where':'simulator: choose',
                                'data': {'task':task,
                                        'bq_indx': index,
                                        },                                
                                        })
            time.sleep(self.timer)
        if config.settings['verbosity']:
            s =f'\nTask {task.id} is chosen:\n['
            for t in self.batch_queue.list:
                s += f'{t.id} , '
            s+=']'
            config.log.write(s)
        return task
    
    
    def defer(self, task):
        if config.time.gct() > task.deadline:
            self.drop(task)
            return 1
        if config.gui==1:
            self.decision.emit({'type':'defer',
                            'time':config.time.gct(),
                            'where':'simulator: defer',
                            'data': {'task':task,                                    
                                    },                            
                                    })
            time.sleep(self.sleep_time)
        self.unmapped_task.pop()
        task.status =  TaskStatus.DEFERRED
        task.no_of_deferring += 1
        self.batch_queue.put(task)
         
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
        if config.gui==1:
            self.decision.emit({'type':'cancelled',
                                'time':config.time.gct(),
                                'where':'simulator: drop',
                                'data': {'task':task,                                    
                                        },                               
                                        })
            time.sleep(self.sleep_time)

        if config.settings['verbosity']:       
            s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
                task.id, config.time.gct())
            config.log.write(s)
        self.gui_machine_log.append({"Task id":task.id,"Event Type":"CANCELLED","Time":config.time.gct(), "Type":'task'})

    def map(self, machine):
        task = self.unmapped_task.pop()
        assignment = machine.local_scheduler.admit(task)
        if assignment != 'notEmpty':
            task.assigned_machine = machine
            self.stats['mapped'].append(task)
            if config.gui==1:
                self.decision.emit({'type':'map',
                                'time':config.time.gct(),
                                'where':'scheduler: map',
                                'data': {'task':task,
                                         'assigned_machine':machine,                                    
                                        },
                                        })
                time.sleep(self.sleep_time)
        else:
            self.defer(task)

    
    def low_priority_queue(self):
        low_priority_tt = []        
        values = []
        
        for tt in config.task_types:
            arrived = self.stats[f'{tt.name}-arrived']

            completed = 0
            for machine in config.machines:                
                completed += machine.stats[f'{tt.name}-completed']
            if arrived > 0 :
                value = completed / arrived              
            else:
                value = 0.0
            self.stats[f'{tt.name}-overall'] = value
            values.append(value)
        values = np.array(values)
        mean = values.mean()
        std = values.std()

        # for tt in config.task_types:
        #     value = self.stats[f'{tt.name}-overall']
        #     if mean > value :                
        #         low_priority_tt.append(tt)

        for tt in config.task_types:
            value = self.stats[f'{tt.name}-overall']
            if value < (mean - config.fairness_factor* std) :                
                low_priority_tt.append(tt)


        # low_priority_tt = []
        # for tt in Config.task_types:
        #     if tt.name == 'TT2':
        #         #print('TT2')
        #         low_priority_tt.append(tt)
                 
            
        return low_priority_tt
    
    def phase1(self):
        deadline_met = []
        provisional_map = []

        low_priority_tt = self.low_priority_queue()         

        index = 0 
        for task in self.batch_queue.list:            
            machines_met_deadline = []  
            
            for machine in config.machines:                
                pct = machine.provisional_map(task)               
                
                if pct < task.deadline:                                                        
                    machines_met_deadline.append(machine)

            if not machines_met_deadline and task.type in low_priority_tt:
                    
                    fastest_machine = min(task.estimated_time, key =task.estimated_time.get )
                    for machine in config.machines:
                        if machine.type.name == fastest_machine:
                            fastest_machine = machine                    
                    
                    for candid_for_drop in reversed(fastest_machine.queue.list):
                        if candid_for_drop.type not in low_priority_tt:                                                      
                            fastest_machine.local_scheduler.cancel(candid_for_drop)
                        pct = fastest_machine.provisional_map(task)
                        if pct < task.deadline:                         
                            machines_met_deadline.append(machine)
                            break   

            
            deadline_met.append([task,index,machines_met_deadline])
            index += 1
        
        for item in deadline_met:
            task = item[0]
            index = item[1]
            machines = item[2]
            min_ec = float('inf')
            min_ec_machine = None 
            
            for machine in machines: 
                pec = machine.specs['power'] * task.estimated_time[machine.type.name]                           
                if pec < min_ec:
                    min_ec = pec
                    min_ec_machine = machine                
            provisional_map.append([task, min_ec, min_ec_machine, index])
            
        return provisional_map
    

    def phase2(self, provisional_map):
        provisional_map_machines = []
        low_priority_tt = self.low_priority_queue()
        low_priority_map = []
        high_priority_map = []

        for pair in provisional_map:
            task = pair[0]
            if task.type in  low_priority_tt:
                low_priority_map.append(pair)
            else:
                high_priority_map.append(pair)
        # rnd = np.random.random()
        # if (rnd < config.fairness_factor) and (low_priority_map):
        #     provisional_map = low_priority_map
        if low_priority_map:
            provisional_map = low_priority_map
              
        for machine in config.machines:                   
            if not machine.queue.full():
                min_ec =float('inf')
                task = None
                index = None 
                for pair in provisional_map:                                                         
                    if pair[2] != None and machine.id == pair[2].id and pair[1] < min_ec:
                        task = pair[0]
                        min_ec = pair[1]
                        index = pair[3]
                provisional_map_machines.append([task,machine,min_ec,index ])        
        return provisional_map_machines


    def schedule(self):        
        provisional_map = self.phase1()
        self.gui_machine_log = []
        for item in provisional_map:
            #print(item[0].id, item[2].type.name)
            task = item[0]
            machine = item[2]
            
            if  machine == None:
                index = self.batch_queue.list.index(task)
                task = self.choose(index)                
                if task.no_of_deferring <= 2:
                    self.defer(task)                    

                else:                    
                    self.drop(task)   
                            
        provisional_map_machines = self.phase2(provisional_map)      
        
        for pair in provisional_map_machines:               
            task = pair[0]
            assigned_machine = pair[1]
            
            if task != None :                  
                index = self.batch_queue.list.index(task)                                               
                task = self.choose(index)
                self.map(assigned_machine)
                
                return assigned_machine
                
            
        return None
            
    #####
    