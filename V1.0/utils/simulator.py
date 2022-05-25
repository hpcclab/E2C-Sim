"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
import pandas as pd
import csv

import utils.config as config
from utils.event import Event, EventTypes
from utils.task import Task
from utils.schedulers.EE import EE
from utils.schedulers.MM import MM
from utils.schedulers.MSD import MSD
from utils.schedulers.MMU import MMU
from utils.schedulers.FEE import FEE
from utils.schedulers.FCFS import FCFS


class Simulator:
    #def __init__(self, workload_id, epsiode_no, id = 0):               
    def __init__(self, het_level, workload_id, epsiode_no, id = 0):               
        self.path_to_arrival = f"{config.settings['path_to_workload']}/workloads/H-{het_level}/workload-{workload_id}/workload-{epsiode_no}.csv"
        #self.path_to_arrival = f"{config.settings['path_to_workload']}/workloads/workload-{workload_id}/workload-{epsiode_no}.csv"
        self.verbosity = config.settings['verbosity']
        self.id = id
        self.tasks = []
        self.total_no_of_tasks = []
        self.energy_statistics = []
        

    def create_event_queue(self):        
        df = pd.read_csv(self.path_to_arrival)
        est_clmns =[]
        ext_clmns = []

        for machine_type in config.machine_types:
            column_name = f'est_{machine_type.name}'
            column_idx = df.columns.get_loc(column_name)
            est_clmns.append(column_idx)
            for r in range(1,machine_type.replicas+1):
                column_name = f'ext_{machine_type.name}-{r}'
                column_idx = df.columns.get_loc(column_name)
                ext_clmns.append(column_idx)


        for idx, row in df.iterrows():
            task_id = idx
            task_type_id = int(row['task_type_id'])            
            arrival_time = row['arrival_time']
            d_est = {}
            d_real = {}

            
            
            for est_clmn in est_clmns:
                d_est[df.columns[est_clmn].split('_')[1]] = row[est_clmn]            

            for ext_clmn in ext_clmns:
                d_real[df.columns[ext_clmn].split('_')[1]] = row[ext_clmn]          
           
            
            estimated_time = d_est
            execution_time = d_real
            type = config.find_task_type(task_type_id)
            self.tasks.append(Task(task_id, type, estimated_time,
                                      execution_time, arrival_time))    
        
        self.total_no_of_tasks = len(self.tasks)
        for task in self.tasks:
            event = Event(task.arrival_time, EventTypes.ARRIVING, task)
            config.event_queue.add_event(event)
        

    def set_scheduling_method(self):
        if config.scheduling_method == 'EE':
            self.scheduler = EE(self.total_no_of_tasks)
        # elif self.scheduling_method == 'ME':
        #     self.scheduler = ME(self.total_no_of_tasks)
        elif config.scheduling_method == 'MM':
            self.scheduler = MM(self.total_no_of_tasks)
        elif config.scheduling_method == 'FEE':
            self.scheduler = FEE(self.total_no_of_tasks)
        elif config.scheduling_method == 'MSD':
            self.scheduler = MSD(self.total_no_of_tasks)
        elif config.scheduling_method == 'MMU':
            self.scheduler = MMU(self.total_no_of_tasks)
        # elif self.scheduling_method == 'RND':
        #     self.scheduler = RND(self.total_no_of_tasks)        
        elif config.scheduling_method == 'FCFS':
            self.scheduler = FCFS(self.total_no_of_tasks)
        # elif self.scheduling_method == 'RLS':
        #     self.scheduler = RLS(self.total_no_of_tasks)
        # elif self.scheduling_method == 'TabRLS':
        #     self.scheduler = TabRLS(self.total_no_of_tasks)

        else:
            print('ERROR: Scheduler ' + config.scheduling_method + ' does not exist')
            self.scheduler = None
        
    def idle_energy_consumption(self):
        for machine in config.machines:
                idle_time_interval = config.time.gct() - machine.idle_time
                if idle_time_interval >0:
                    idle_energy_consumption = machine.specs['idle_power'] * idle_time_interval                    
                    machine.idle_time = config.time.gct()
                else:
                    idle_energy_consumption = 0.0

                machine.stats['idle_energy_usage'] += idle_energy_consumption
                machine.stats['energy_usage'] += idle_energy_consumption
                config.available_energy -= idle_energy_consumption
                s = '\nmachine {} @{}\n\tidle_time:{}\n\tidle_time_interval:{}\n\tidle power consumption: {} '.format(
                    machine.id, config.time.gct(), machine.idle_time, idle_time_interval, idle_energy_consumption)
                #config.log.write(s)


    def run(self):       
         
        while config.event_queue.event_list and config.available_energy > 0.0:
        
            self.idle_energy_consumption()
            event = config.event_queue.get_first_event()
            task = event.event_details
            config.time.sct(event.time)
            if self.verbosity:
                s = '\n\n*****Task:{} \t\t {}  @time:{}'.format(
                    task.id, event.event_type.name, event.time)
                config.log.write(s)
                #print(s)

            row =[config.time.gct(),config.available_energy]

            for machine in config.machines:                
                row.append(machine.stats['energy_usage'])
            self.energy_statistics.append(row)


            if event.event_type == EventTypes.ARRIVING:                
                self.scheduler.batch_queue.put(task)
                self.scheduler.stats[f'{task.type.name}-arrived'] += 1
                assigned_machine = self.scheduler.schedule()                

            elif event.event_type == EventTypes.DEFERRED:
                # self.scheduler.batch_queue.put(task)                
                assigned_machine = self.scheduler.schedule()
                

            elif event.event_type == EventTypes.COMPLETION:                
                machine = task.assigned_machine
                machine.terminate(task)                
                self.scheduler.schedule()

            # elif event.event_type == EventTypes.OFFLOADED:
            #     if self.verbosity >= 1:
            #         pbar.update(1)
            #     Config.cloud.terminate(task)
            #     self.scheduler.feed()
            #     num = 4
            #     assigned_machine = self.scheduler.schedule()
            elif event.event_type == EventTypes.DROPPED_RUNNING_TASK:
                machine = task.assigned_machine
                machine.drop()
                self.scheduler.schedule()            
         
        
    def report(self, path_to_report):        
        
        detailed_header = ['id','type','urgency','status','assigned_machine', 
                'arrival_time','execution_time','energy_usage','start_time',
                'completion_time','missed_time','deadline',
                'extended_deadline']
        detailed = open(f'{path_to_report}/detailed-{self.id}.csv','w')
        detailed_writer = csv.writer(detailed)
        detailed_writer.writerow(detailed_header)

        for task in self.tasks:
            if task.assigned_machine == None:
                assigned_machine = None
            else:
                assigned_machine = f'{task.assigned_machine.type.name}-{task.assigned_machine.replica_id}'
            
            detailed_row = [
                task.id,
                task.type.name,
                task.urgency.name,
                task.status.name,
                assigned_machine, 
                task.arrival_time,
                task.execution_time,
                task.energy_usage,
                task.start_time,
                task.completion_time,
                task.missed_time,
                task.deadline - task.devaluation_window,
                task.deadline
            ]       

            detailed_writer.writerow(detailed_row)            
        
        total_assigned_tasks = 0
        total_completion = 0
        total_xcompletion = 0
        missed_urg = 0
        missed_be = 0
        total_wasted_energy = 0 
        

        for machine in config.machines:
            total_assigned_tasks += machine.stats['assigned_tasks']
            total_completion += machine.stats['completed_tasks']
            total_xcompletion += machine.stats['xcompleted_tasks']
            total_wasted_energy += machine.stats['wasted_energy']
            missed_urg += machine.stats['missed_URG_tasks']
            missed_be += machine.stats['missed_BE_tasks']

            completed_percent = 0
            xcompleted_percent = 0                        
            energy_percent = machine.stats['energy_usage'] / config.total_energy
            wasted_energy = machine.stats['wasted_energy']
            if machine.stats['assigned_tasks'] != 0:
                completed_percent = machine.stats['completed_tasks'] / machine.stats['assigned_tasks']
                xcompleted_percent = machine.stats['xcompleted_tasks'] / machine.stats['assigned_tasks']
                

            s = '\nMachine: {:} (id#{:})  \n\t%Completion: {:2.1f} #: {:}\n\t%XCompletion:{:2.1f} #: {:}\n\t#Missed URG:{:1.2f}\n\tMissed BE:{:}\n\t%Energy: {:2.1f}\n\t%Wasted Energy: {:2.1f} '.format(
                machine.type.name,machine.id,
                100*completed_percent, machine.stats['completed_tasks'],
                100*xcompleted_percent, machine.stats['xcompleted_tasks'],
                machine.stats['missed_URG_tasks'],
                machine.stats['missed_BE_tasks'],
                100*energy_percent,
                100 * wasted_energy)
            # if self.verbosity <= 3 :
            #     print(s)
            config.log.write(s)

        total_completion_percent = 100 * (total_completion / self.total_no_of_tasks)
        total_xcompletion_percent = 100 * (total_xcompletion / self.total_no_of_tasks)
        total_wasted_energy_percent = 100 * (total_wasted_energy / config.total_energy)
        s = '\n%Total Completion: {:2.1f}'.format(total_completion_percent)
        s += '\n%Total xCompletion: {:2.1f}'.format(total_xcompletion_percent)
        s += '\n%deferred: {:2.1f}'.format(len(self.scheduler.stats['deferred']))
        s += '\n%dropped: {:2.1f}'.format(len(self.scheduler.stats['dropped']))
       
        # if self.verbosity <= 3:
        #     print(s)
        config.log.write(s)

        
        d = {}
        for task_type in config.task_types:            
            for machine in config.machines:
                d [f'{task_type.name}_assigned_to_{machine.type.name}_{machine.replica_id}'] = 0
                d[f'{task_type.name}_completed_{machine.type.name}_{machine.replica_id}']=0
                d[f'{task_type.name}_xcompleted_{machine.type.name}_{machine.replica_id}'] = 0
                d[f'{task_type.name}_missed_{machine.type.name}_{machine.replica_id}']=0
                d[f'{task_type.name}_energy_{machine.type.name}_{machine.replica_id}']=0
                d[f'{task_type.name}_wasted-energy_{machine.type.name}_{machine.replica_id}']=0
        #print(d.keys())
            
        # for task in self.tasks:            
        #     if task.assigned_machine != None:
        #         machine = task.assigned_machine                
        #         d[f'{task.type.name}_assigned_to_{machine.type.name}_{machine.replica_id}'] +=1                
        #         d[f'{task.type.name}_energy_{machine.type.name}_{machine.replica_id}'] += task.energy_usage
        #         d[f'{task.type.name}_wasted-energy_{machine.type.name}_{machine.replica_id}'] += task.wasted_energy
        #         if task.status.name == 'COMPLETED':
        #             d[f'{task.type.name}_completed_{machine.type.name}_{machine.replica_id}'] +=1
        #         elif task.status.name == 'XCOMPLETED':
        #             d[f'{task.type.name}_xcompleted_{machine.type.name}_{machine.replica_id}'] +=1
        #         elif task.status.name == 'MISSED':
        #             d[f'{task.type.name}_missed_{machine.type.name}_{machine.replica_id}'] +=1
        
        # task_report = pd.DataFrame(d, index= [self.id])
        
        # task_report.iloc[:,:-2] /= (0.01*self.total_no_of_tasks)
        # task_report.iloc[:,-2:] /= (0.01*config.total_energy)
        # task_report = task_report.round(3)
        
        row = []
        consumed_energy = config.total_energy - config.available_energy
        no_of_completed_task = self.total_no_of_tasks*0.01*(total_completion_percent+total_xcompletion_percent)
        if no_of_completed_task != 0:
            energy_per_completion = consumed_energy / no_of_completed_task
            energy_per_completion = 100*(energy_per_completion/ config.total_energy)
        elif consumed_energy != 0 and no_of_completed_task == 0:
            energy_per_completion = float('inf')
        else:
            energy_per_completion = 0.0

        row.append(
            [self.id,self.total_no_of_tasks ,
            total_assigned_tasks, len(self.scheduler.stats['dropped']),
            missed_urg,
            missed_be,
            total_completion_percent, total_xcompletion_percent,
            total_completion_percent+total_xcompletion_percent,
            total_wasted_energy_percent,
            100*(consumed_energy/config.total_energy),            
            energy_per_completion ])
        
        #return row, task_report
        return row
