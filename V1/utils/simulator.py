"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
import pandas as pd
import sqlite3 as sq
import csv
import os
import time
import utils.config as config
from utils.event import Event, EventTypes
from utils.event_queue import EventQueue
from utils.execution_time import ExecutionTime
from utils.task import Task
from utils.schedulers.EE import EE
from utils.schedulers.MM import MM
from utils.schedulers.MSD import MSD
from utils.schedulers.MMU import MMU
from utils.schedulers.FEE import FEE
from utils.schedulers.FCFS import FCFS
from utils.schedulers.FCFS_NQ import FCFS_NQ
from utils.schedulers.MECT import MECT
from utils.schedulers.MEET import MEET
from PyQt5.QtCore import pyqtSignal,QObject
from PyQt5.QtCore import QTimer

from utils.db_workload import *
from utils.utilities import *
from utils.initTables import *
from utils.initTables import initTables
import utils.workload as wl


class Simulator(QObject):
    event_signal = pyqtSignal(dict)
    simulation_done = pyqtSignal()
    increment = pyqtSignal()
    
    def __init__(self, path_to_arrivals, path_to_etc, path_to_reports, seed=1):     
        super(Simulator, self).__init__()  

        db_path = './utils/e2cDB.db' 
        self.conn = sq.connect(db_path)
        self.cur = self.conn.cursor()

        self.path_to_arrivals = path_to_arrivals
        self.path_to_etc= path_to_etc
        print("--------------------")
        printTable(self.cur,"workload") 
        print("--------------------")
        self.arrivals = pd.read_sql_query("SELECT * FROM workload", self.conn)
                                                                                
        self.path_to_reports = path_to_reports                
        self.seed = seed  
        self.execution_time_var = 0.05
        self.verbosity = 3
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
        config.event_queue = EventQueue()
        for machine in config.machines:
            machine.reset()
        
	
    def simulate_pause(self, val):
        self.pause = val
    

    def create_event_queue(self): 
        etc = pd.read_csv(self.path_to_etc,index_col=0)
        arrivals = self.arrivals

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
                #arrival_time = 0.0                
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
        config.event_queue.event_list = []
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
        elif scheduling_method == 'FCFS_NQ':
            self.scheduler = FCFS_NQ(self.total_no_of_tasks) 
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
        print(f'len events: {len(config.event_queue.event_list)}')

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
            summary = self.report()
            with open(f'{self.path_to_reports}/{config.scheduling_method}/results-summary.csv','w')  as report_summary:
                report_header = ['workload_path', 'total_no_of_tasks','mapped','cancelled','URG_missed','BE_missed','Completion%','xCompletion%','totalCompletion%','wasted_energy%','consumed_energy%','energy_per_completion%']
                report = csv.writer(report_summary)  
                report.writerow(report_header)
                report.writerows(summary)
            

        #config.log.close()

            
    def report(self,is_detailed = True):     
        path_to_report = f'{self.path_to_reports}/{self.scheduler.name}'        
        os.makedirs(path_to_report, exist_ok = True)        
        if is_detailed:  
            detailed_header = ['id','type','urgency','status','assigned_machine', 
                    'arrival_time','execution_time','energy_usage','start_time',
                    'completion_time','missed_time','deadline',
                    'extended_deadline']
            
            if config.gui:
                try:

                    files = [x for x in os.listdir(f'{path_to_report}/') if x.endswith('csv')]
                except:
                    files = []
                new_file = 'detailed.csv'
                i=1
                while files and (new_file in files):
                    new_file = f'detailed-copy({i}).csv'
                    i+=1
            else:

                workload_id = self.path_to_arrivals.split('/')[-1].split('-')[-1].split('.')[0]
                new_file = f'detailed-{workload_id}.csv'

            detailed = open(f'{path_to_report}/{new_file}','w')
            detailed_writer = csv.writer(detailed)
            detailed_writer.writerow(detailed_header)

            for task in self.tasks:
                if task.assigned_machine == None:
                    assigned_machine = None
                else:
                    assigned_machine = f'{task.assigned_machine.type.name}-{task.assigned_machine.replica_id}'
                
                detailed_row = [
                    task.id,task.type.name,task.urgency.name,
                    task.status.name,assigned_machine, task.arrival_time,
                    task.execution_time,task.energy_usage,task.start_time,
                    task.completion_time,task.missed_time,
                    task.deadline - task.devaluation_window, task.deadline]       

                detailed_writer.writerow(detailed_row) 
            detailed.close()           
        
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
            energy_percent = 100 * (machine.stats['energy_usage'] / config.total_energy)
            wasted_energy_percent = 100 * (machine.stats['wasted_energy'] / config.total_energy)
            if machine.stats['assigned_tasks'] != 0:
                completed_percent = 100 * (machine.stats['completed_tasks'] / machine.stats['assigned_tasks'])
                xcompleted_percent = 100 *(machine.stats['xcompleted_tasks'] / machine.stats['assigned_tasks'])

            s = '\nMachine: {:} (id#{:})  \n\t%Completion: {:2.1f} #: {:}\n\t%XCompletion:{:2.1f} #: {:}\n\t#Missed URG:{:1.2f}\n\tMissed BE:{:}\n\t%Energy: {:2.1f}\n\t%Wasted Energy: {:2.1f} '.format(
                machine.type.name,machine.id,
                completed_percent, machine.stats['completed_tasks'],
                xcompleted_percent, machine.stats['xcompleted_tasks'],
                machine.stats['missed_URG_tasks'],
                machine.stats['missed_BE_tasks'],
                energy_percent,
                wasted_energy_percent)
            
            
                      
            # if self.verbosity <= 3 :
            #print(s)
            config.log.write(s)

        total_completion_percent = 100 * (total_completion / self.total_no_of_tasks)
        total_xcompletion_percent = 100 * (total_xcompletion / self.total_no_of_tasks)
        total_wasted_energy_percent = 100 * (total_wasted_energy / config.total_energy)
        s = '\n%Total Completion: {:2.1f}'.format(total_completion_percent)
        s += '\n%Total xCompletion: {:2.1f}'.format(total_xcompletion_percent)
        s += '\n%deferred: {:2.1f}'.format(len(self.scheduler.stats['deferred']))
        s += '\n%dropped: {:2.1f}'.format(len(self.scheduler.stats['dropped']))
        
        # if self.verbosity <= 3:
        print(s)
        config.log.write(s)

        # d = {}
        # for task_type in config.task_types:
        #     for machine in config.machines:
        #         d [f'{task_type.name}_assignedto{machine.type.name}_{machine.replica_id}'] = 0
        #         d[f'{task_type.name}completed{machine.type.name}_{machine.replica_id}']=0
        #         d[f'{task_type.name}xcompleted{machine.type.name}_{machine.replica_id}'] = 0
        #         d[f'{task_type.name}missed{machine.type.name}_{machine.replica_id}']=0
        #         d[f'{task_type.name}energy{machine.type.name}_{machine.replica_id}']=0
        #         d[f'{task_type.name}wasted-energy{machine.type.name}_{machine.replica_id}']=0
    
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
            [self.path_to_arrivals,self.total_no_of_tasks ,
            total_assigned_tasks, len(self.scheduler.stats['dropped']),
            missed_urg,
            missed_be,
            total_completion_percent, total_xcompletion_percent,
            total_completion_percent+total_xcompletion_percent,
            total_wasted_energy_percent,
            100*(consumed_energy/config.total_energy),            
            energy_per_completion ])       
        config.log.close()
        #print(row)
        return row
    
    