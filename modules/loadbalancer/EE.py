"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus
from utils.base_scheduler import BaseScheduler
from utils.event import Event, EventTypes
import utils.config as config
import time


class EE(BaseScheduler):
    
    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.name = 'EE'
        self.total_no_of_tasks = total_no_of_tasks
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
            time.sleep(self.sleep_time)
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
        if config.event_queue.event_list:
            event_time = config.event_queue.event_list[0].time
        else:
            event_time = config.time.gct()
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
                task.id, config.time.gct()       )
            s+= f'\nNo of Deferring: {task.no_of_deferring}'
            config.log.write(s)
        self.gui_machine_log.append({"Task id":task.id,"Event Type":"CANCELLED","Time":config.time.gct(), "Type":'task'})

    def map(self, machine):
        task = self.unmapped_task.pop()
        assignment = machine.admit(task)
        print(assignment)
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
    
    def phase1(self):
        
        deadline_met = []
        provisional_map = []
        
        index = 0 
        for task in self.batch_queue.list:            
            machines_met_deadline = []  
            
            for machine in config.machines:                
                pct = machine.provisional_map(task)               
                #print(f'task:{task.id} machine:{machine.type.name} pct:{pct}')
                if pct < 1.0* task.deadline:                                                        
                #if pct < 10000.1*task.deadline:                                                        
                    machines_met_deadline.append(machine)
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
                #pec = machine.provisional_map(task)                           
                if pec < min_ec:
                    min_ec = pec
                    min_ec_machine = machine                
            provisional_map.append([task, min_ec, min_ec_machine, index])
        
        return provisional_map
    

    def phase2(self, provisional_map):
        provisional_map_machines = []        
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
        self.gui_machine_log = []
        if config.settings['verbosity']:
            s = f'\nCurrent State @{config.time.gct()}'
            s += '\nBQ = '
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
        
        if config.settings['verbosity']:
            s = '\nPHASE-I:\n'        
            pairs = [[pair[0].id, pair[2].type.name, pair[3]] for pair in provisional_map if pair[2] != None]
            pairs_none = [[pair[0].id, None, pair[3]] for pair in provisional_map if pair[2] == None]
            
            s+= f'Feasibles: {pairs}\nNOT-Feasible: {pairs_none}'

            config.log.write(s)
        
        for item in provisional_map:
            #print(item[0].id, item[2].type.name)
            task = item[0]
            machine = item[2]
            
            if  machine == None:
                # if config.settings['verbosity']:
                #     s = f'\ntask {task.id} is not feasible!'
                #     config.log.write(s)
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
                # s = f"\ntask:{task.id}  assigned to:{assigned_machine.type.name}  ec:{pair[2]}   delta:{task.deadline}"
                # config.log.write(s)
                
                return assigned_machine
                
            
        return None
            
    #####
    