"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
import pandas as pd
import csv
import os
import time
import utils.config as config
from utils.event import Event, EventTypes
from utils.execution_time import ExecutionTime
from utils.task import Task
from utils.schedulers.EE import EE
from utils.schedulers.MM import MM
from utils.schedulers.MSD import MSD
from utils.schedulers.MMU import MMU
from utils.schedulers.FEE import FEE
from utils.schedulers.FCFS import FCFS
from utils.schedulers.MECT import MECT
from utils.schedulers.MEET import MEET
from PyQt5.QtCore import pyqtSignal,QObject
from PyQt5.QtCore import QTimer
from utils.report import report as reporter

class Simulator(QObject):
    event_signal = pyqtSignal(dict)
    simulation_done = pyqtSignal()
    increment = pyqtSignal()
    
    def __init__(self, path_to_arrivals, path_to_etc, path_to_reports, seed=1):     
        super(Simulator, self).__init__()  
        self.path_to_arrivals = path_to_arrivals
        self.path_to_etc= path_to_etc
        self.path_to_reports = path_to_reports                
        self.seed = seed  
        self.execution_time_var = 0.05
        self.verbosity = config.verbosity
        self.tasks = []
        self.total_no_of_tasks = None
        self.energy_statistics = []
        self.sleep_time = 0.1
        self.set_scheduling_method(config.scheduling_method)
        self.pause = False
        self.is_incremented = False
    
    def reset(self):
        config.time.sct(0.0)
        config.available_energy = config.total_energy
        for machine in config.machines:
            machine.reset()
        
	
    def simulate_pause(self, val):
        self.pause = val
    

    def create_event_queue(self): 
        print(self.path_to_arrivals)      
        arrivals = pd.read_csv(self.path_to_arrivals) 
        etc = pd.read_csv(self.path_to_etc,index_col=0)
                
        execution_time = ExecutionTime(self.seed)
        with open(f'{os.path.dirname(self.path_to_etc)}/execution_times.csv','w') as et_file:
            et_writer = csv.writer(et_file)
            header = ['task_type']
            for machine_type in config.machine_types:
                    for r in range(1,machine_type.replicas+1):
                        header.append(f'{machine_type.name}_{r}')
            et_writer.writerow(header)
            for idx, row in arrivals.iterrows():                                                
                task_id = idx
                task_type_name = row['task_type']
                arrival_time = row['arrival_time']  
                estimated_times = etc.loc[task_type_name,:].to_dict()
                execution_times = {}
                execution_times_li = [task_type_name]
                for mt_id, machine_type in enumerate(config.machine_types):
                    for r in range(1,machine_type.replicas+1): 
                        execution_time.seed += idx * mt_id + r                    
                        execution_times[f'{machine_type.name}-{r}'] = execution_time.synthesize(etc, task_type_name, machine_type.name, self.execution_time_var)
                        execution_times_li.append(execution_times[f'{machine_type.name}-{r}'])
                    
                et_writer.writerow( execution_times_li)
            
                type = config.find_task_type(task_type_name)
                self.tasks.append(Task(task_id, type, estimated_times,
                                        execution_times, arrival_time))
               
        
        self.total_no_of_tasks = len(self.tasks)
        for task in self.tasks:            
            event = Event(task.arrival_time, EventTypes.ARRIVING, task)
            config.event_queue.add_event(event)
        return config.event_queue
        
    def set_scheduling_method(self, scheduling_method):
        if scheduling_method == 'EE':
            self.scheduler = EE(self.total_no_of_tasks)        
        elif scheduling_method == 'MM':
            self.scheduler = MM(self.total_no_of_tasks)
        elif scheduling_method == 'FEE':
            self.scheduler = FEE(self.total_no_of_tasks)
        elif scheduling_method == 'MSD':
            self.scheduler = MSD(self.total_no_of_tasks)
        elif scheduling_method == 'MMU':
            self.scheduler = MMU(self.total_no_of_tasks)              
        elif scheduling_method == 'FCFS':
            self.scheduler = FCFS(self.total_no_of_tasks) 
        elif scheduling_method == 'MECT':
            self.scheduler = MECT(self.total_no_of_tasks) 
        elif scheduling_method == 'MEET':
            self.scheduler = MEET(self.total_no_of_tasks)
        else:
            print('ERROR: Scheduler ' + config.scheduling_method + ' does not exist')
            self.scheduler = None
        #self.scheduler.decision.connet(self.event_signal)
        
            
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
        self.create_event_queue()

        while config.event_queue.event_list and config.available_energy > 0.0:               
            while config.gui==1 and (self.pause and self.is_incremented):               
                time.sleep(0.0)
            self.idle_energy_consumption()
            event = config.event_queue.get_first_event()
            task = event.event_details
            config.time.sct(event.time)
            if self.verbosity:
                s = f'\n\n*****Task:{task.id} \t\t {event.event_type.name}  @time:{event.time}'
                config.log.write(s)   
                #print(s)

            row =[config.time.gct(),config.available_energy]
            for machine in config.machines:                
                row.append(machine.stats['energy_usage'])
            self.energy_statistics.append(row)
  
            if event.event_type == EventTypes.ARRIVING:                
                self.scheduler.batch_queue.put(task)
                if config.gui == 1:     
                    self.event_signal.emit({'type':'arriving',
                                            'time':event.time,
                                            'where':'simulator: arriving',
                                            'data':{'task':task,                                                    
                                                    },                                            
                                                    })
                    time.sleep(self.sleep_time)
                self.scheduler.stats[f'{task.type.name}-arrived'] += 1                
                assigned_machine = self.scheduler.schedule()

            elif event.event_type == EventTypes.DEFERRED:
                assigned_machine = self.scheduler.schedule()
            
            elif event.event_type == EventTypes.COMPLETION:               
                machine = task.assigned_machine 
                machine.terminate(task)                             
                self.scheduler.schedule()
                
            elif event.event_type == EventTypes.DROPPED_RUNNING_TASK:
                machine = task.assigned_machine
                machine.drop()     
                self.scheduler.schedule()
            
            if self.pause:
                self.is_incremented = True
        
         
                

        # if config.gui == 1: 
        #     print(20*'-')
        #     for task in self.tasks:
        #         print(f'{task.id} : {task.status}')  
            # self.simulation_done.emit()

        
        if config.gui :
            self.simulation_done.emit()
            summary = reporter(self.path_to_reports, self.path_to_arrivals, self.scheduler, self.total_no_of_tasks, self.tasks)
            if not os.path.exists(f'{self.path_to_reports}/{config.scheduling_method}/'):
                os.makedirs(f'{self.path_to_reports}/{config.scheduling_method}/')
            with open(f'{self.path_to_reports}/{config.scheduling_method}/results-summary.csv','w')  as report_summary:
                report_header = ['workload_path', 'total_no_of_tasks','mapped','cancelled','URG_missed','BE_missed','Completion%','xCompletion%','totalCompletion%','wasted_energy%','consumed_energy%','energy_per_completion%']
                report = csv.writer(report_summary)  
                report.writerow(report_header)
                report.writerows(summary)
            

        #config.log.close()