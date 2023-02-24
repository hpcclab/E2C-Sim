"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus, UrgencyLevel
from utils.base_scheduler import BaseScheduler
import Config

import numpy as np


class RND(BaseScheduler):
    machine_index = 0

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.total_no_of_tasks = total_no_of_tasks
        self.name = 'RND'        

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
        self.unmapped_task = -1
        task.no_of_deferring += 1 
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
        random_map = []
        index = 0 
        for task in self.batch_queue: 
            available_machines = []                     
            if task != -1: 
                for machine in Config.machines:                   
                    if machine.notfull():                   
                        available_machines.append(machine)
                if available_machines:
                    random_machine = np.random.choice(available_machines)
                else:
                    random_machine = -1
                random_map.append([task,random_machine, index])
            index += 1
        
        return random_map
    

    def phase2(self, random_map):
        random_map_machines = []
        assigned_tasks = []       
        for machine in Config.machines:            
            if -1 in machine.queue:                
                assigned_tasks = []                
                for pair in random_map:                                      
                    if pair[1] != -1 and machine.id == pair[1].id:
                        task = pair[0]
                        index = pair[2]
                        assigned_tasks.append([task,index])
                    
                if assigned_tasks:                                    
                    idx = np.random.choice(len(assigned_tasks))
                    random_map_machines.append([assigned_tasks[idx][0],machine, assigned_tasks[idx][1]])                    
                        
                

        return random_map_machines



    def schedule(self):        
        provisional_map = self.phase1() 
        provisional_map_machines = self.phase2(provisional_map)      
        

        for pair in provisional_map_machines:
            task = pair[0]
            assigned_machine = pair[1]            
            
            if task != -1 :   
                index = 0
                for t in self.batch_queue:
                    if t != -1 and t.id == task.id:
                        break
                    index += 1
                self.choose(index)                
                self.map(assigned_machine)
                return assigned_machine
            
    #####
    