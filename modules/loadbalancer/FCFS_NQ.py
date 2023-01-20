"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus
from utils.base_scheduler import BaseScheduler
import utils.config as config
from utils.queue import Queue
from utils.event import Event, EventTypes
import time


class FCFS_NQ(BaseScheduler):
    
    
    def __init__(self, total_no_of_tasks):
        super(FCFS_NQ, self).__init__()
        self.name = 'FCFS_NQ'
        self.total_no_of_tasks = total_no_of_tasks
        self.prev_assignment_idx = -1
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
        self.unmapped_task.pop()
        if config.gui==1:
                self.decision.emit({'type':'defer',
                                'time':config.time.gct(),
                                'where':'simulator: defer',
                                'data': {'task':task,                                    
                                        },                            
                                        })
                time.sleep(self.sleep_time)
        task.status =  TaskStatus.DEFERRED
        task.no_of_deferring += 1
        self.batch_queue.insert(0, task)

        # event_time = config.event_queue.event_list[0].time
        # event_type = EventTypes.DEFERRED
        # event = Event(event_time, event_type, task)
        # config.event_queue.add_event(event)
         
        self.stats['deferred'].append(task)
        if config.settings['verbosity']:
            s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
            task.id, config.time.gct())
            config.log.write(s)
        
        

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
            config.log.write(s)
        

    def map(self, machine):
        task = self.unmapped_task.pop()
        assignment,_ = machine.admit(task)
        if assignment != 'notEmpty':
            if config.gui==1:
                self.decision.emit({'type':'map',
                                'time':config.time.gct(),
                                'where':'scheduler: map',
                                'data': {'task':task,
                                         'assigned_machine':machine,                                    
                                        },
                                        })
                time.sleep(self.sleep_time)
            task.assigned_machine = machine
            self.stats['mapped'].append(task)
            s = f"\ntask:{task.id}  assigned to:{task.assigned_machine.type.name}  delta:{task.deadline}"
            config.log.write(s)
        else:
            self.defer(task)            
        
    
    def available_machines(self):
        available_machines_idx = []
        for m_idx, machine in enumerate(config.machines):
            if not machine.is_working():
                available_machines_idx.append(m_idx)
        return available_machines_idx
        
        
        
   
    


    def schedule(self):
        

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

        if self.batch_queue.empty():
            return None
                
        # machine_index = (self.prev_assignment_idx+1) % config.no_of_machines        
        # machine = config.machines[machine_index]
        # self.prev_assignment_idx = machine_index
        available_machines_idx = self.available_machines()

        if available_machines_idx:
            if self.prev_assignment_idx < max(available_machines_idx):
                assigned_machine_idx = min([x for x in available_machines_idx if x> self.prev_assignment_idx])
            else:
                assigned_machine_idx = min(available_machines_idx)
            assigned_machine = config.machines[assigned_machine_idx]
            self.choose()
            self.map(assigned_machine)
            self.prev_assignment_idx = assigned_machine_idx
            return  assigned_machine           
        else:
            task = self.choose()
            self.defer(task)
            return None

        



    