"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus, UrgencyLevel
from utils.base_scheduler import BaseScheduler
import Config


class ME(BaseScheduler):
    machine_index = 0

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.total_no_of_tasks = total_no_of_tasks
        self.name = 'MM'

    def feed(self):

        while self.unlimited_queue and (-1 in self.batch_queue):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task

    def choose(self, index):
              
        if self.batch_queue[index] != -1:
            self.unmapped_task = self.batch_queue[index]
            self.batch_queue = self.batch_queue[:index] + self.batch_queue[index+1:]+[-1]            
            #self.feed()
            return self.unmapped_task
                         
        else:            
            self.unmapped_task = -1
            return -1

    def offload(self, task):
        task.status = task.status_list['offloaded']

    def defer(self, task):
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if Config.current_time > task.deadline + task.devaluation_window:
                self.drop(task)
                return
        elif task.urgency == UrgencyLevel.URGENT:
            if Config.current_time > task.deadline:
                self.drop(task)
                return
        
        if -1 in self.batch_queue:
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task
        else:
            replaced_task = self.batch_queue[-1]
            self.unlimited_queue = [replaced_task] + self.unlimited_queue
            self.batch_queue[-1] = task
        task.status =  TaskStatus.DEFERRED
        self.stats['deferred'].append(task)
        s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
           task.id, Config.current_time        )
        Config.log.write(s)

    def drop(self, task):
        task.status = TaskStatus.CANCELLED
        task.drop_time = Config.current_time
        self.stats['dropped'].append(task)        
        s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
            task.id, Config.current_time        )
        Config.log.write(s)

    def map(self, machine):
        assignment = machine.admit(self.unmapped_task)

        if assignment != 'notEmpty':
            self.unmapped_task.assigned_machine = machine
            self.stats['mapped'].append(self.unmapped_task)
        else:
            self.defer(self.unmapped_task)
    
    def phase1(self):
        provisional_map = []
        index = 0 
        for task in self.batch_queue:            
            if task != -1:                
                min_ec = float('inf')
                min_ec_machine = -1
                for machine in Config.machines:
                    prov_energy_consumption = machine.specs['power'] * task.estimated_time[machine.type.name]                                                            
                    if prov_energy_consumption < min_ec and machine.notfull():
                        min_ec = prov_energy_consumption
                        min_ec_machine = machine                
                provisional_map.append([task, min_ec, min_ec_machine, index])
            index += 1        
        
        
        return provisional_map
    

    def phase2(self, provisional_map):
        provisional_map_machines = []
        
        for machine in Config.machines:
            #print('machine {} : '.format(machine.id))
            if -1 in machine.queue:
                min_ec =float('inf')
                task = -1
                index = -1 
                for pair in provisional_map:                    
                    if machine.id == pair[2].id and pair[1] < min_ec:
                        task = pair[0]
                        min_ec = pair[1]
                        index = pair[3]                        
                #if task != -1:
                    #print('Assigned Task {} to machine {} '.format(task.id, machine.id))
                provisional_map_machines.append([task,machine,index])

        return provisional_map_machines




                



    def schedule(self):
        
        provisional_map = self.phase1()       
        provisional_map_machines = self.phase2(provisional_map)
        
        for pair in provisional_map_machines:
            task = pair[0]
            assigned_machine = pair[1]
            index = pair[2]
            
            
            
            if task != -1 :
                #print('Task {} is mapped to machine {} '.format(task.id, assigned_machine.id))
                self.choose(index)                
                self.map(assigned_machine)
                return assigned_machine
    
    #####
    