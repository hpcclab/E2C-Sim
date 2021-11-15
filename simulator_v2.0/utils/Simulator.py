"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

import Config
from Task import Task
from Event import Event, EventTypes
from FCFS import FCFS
from MM import MM
from MSD import MSD
from MMU import MMU
from RLS import RLS

from TabRLS import TabRLS
from tqdm import tqdm

#from tqdm import tqdm
import numpy as np
import pandas as pd
import csv
import GUI




class Simulator:


    def __init__(self,scheduling_method, path_to_arrival, id = 0, verbosity = 0):
        self.scheduling_method = scheduling_method
        if Config.gui:
            self.gui1 = GUI.Gui("Scheduler GUI", '1000x800', 700, 800)
        self.path_to_arrival = path_to_arrival
        self.verbosity = verbosity
        self.id = id
        self.tasks = []
        self.total_no_of_tasks = []

    def create_event_queue(self):

        with open(self.path_to_arrival, 'r') as data_file:
            for task in data_file:
                task = task.strip()
                task_details = [x.strip() for x in task.split(',')]

                if task[0] == '#':
                    machine_types = [x.split('_')[-1] for x in task.split(',')[4:6]]
                else:
                    task_id = int(task_details[0])
                    task_type_id = int(task_details[1])
                    task_size = float(task_details[2])
                    arrival_time = float(task_details[3])
                    estimated_time = {machine_types[0]: float(task_details[4]),
                                      machine_types[1]: float(task_details[5]),
                                      'CLOUD': float(task_details[6])}
                    execution_time = {machine_types[0]: float(task_details[7]),
                                      machine_types[1]: float(task_details[8]),
                                      'CLOUD': float(task_details[9])}
                    type = Config.find_task_types(task_type_id)
                    self.tasks.append(Task(task_id, type, task_size,estimated_time,
                                           execution_time, arrival_time))
        self.total_no_of_tasks = len(self.tasks)
        for task in self.tasks:
            event = Event(task.arrival_time, EventTypes.ARRIVING, task)
            Config.event_queue.add_event(event)

    def set_scheduling_method(self):
        if self.scheduling_method == 'MM':
            self.scheduler = MM(self.total_no_of_tasks)
        elif self.scheduling_method == 'MSD':
            self.scheduler = MSD(self.total_no_of_tasks)
        elif self.scheduling_method == 'MMU':
            self.scheduler = MMU(self.total_no_of_tasks)
        elif self.scheduling_method == 'FCFS':
            self.scheduler = FCFS(self.total_no_of_tasks)
        elif self.scheduling_method == 'RLS':
            self.scheduler = RLS(self.total_no_of_tasks)
        elif self.scheduling_method == 'TabRLS':
            self.scheduler = TabRLS(self.total_no_of_tasks)

        else:
            print('ERROR: Scheduler ' + self.scheduling_method + ' does not exist')
            self.scheduler = None
        self.gui1.create_main_queue(8, self.scheduling_method)

    def idle_energy_consumption(self):


        for machine in Config.machines:
                idle_time_interval = Config.current_time - machine.idle_time
                if idle_time_interval >0:
                    idle_energy_consumption = machine.specs['idle_power'] * idle_time_interval
                    machine.idle_time = Config.current_time
                else:
                    idle_energy_consumption = 0.0
                machine.stats['energy_usage'] += idle_energy_consumption
                Config.available_energy -= idle_energy_consumption
                s = '\nmachine {} @{}\n\tidle_time:{}\n\tidle_time_interval:{}\n\tidle power consumption: {} '.format(
                    machine.id, Config.current_time, machine.idle_time, idle_time_interval, idle_energy_consumption)
                Config.log.write(s)


    def run(self):

        if Config.gui == 1:
            self.gui1.create_main_queue(8, self.scheduling_method)
            self.gui1.create_machine_names()
            self.gui1.create_legend()
            self.gui1.create_controls()
            self.gui1.create_task_stats(self.total_no_of_tasks)
            self.gui1.create_menubar()
        num = 0
        if self.verbosity == 0:
            pbar = tqdm(total=self.total_no_of_tasks)

        # if self.verbosity <= 1:
        #     pbar = tqdm(total=self.total_no_of_tasks)
        while Config.event_queue.event_list and Config.available_energy > Config.min_energy:
        #while Config.event_queue.event_list :


            self.idle_energy_consumption()
            event = Config.event_queue.get_first_event()
            task = event.event_details
            Config.current_time = event.time
            s = '\nTask:{} \t\t {}  @time:{}'.format(
                task.id, event.event_type.name, event.time)
            Config.log.write(s)


            if self.verbosity == 2 :
                print(s)


            if event.event_type == EventTypes.ARRIVING:


                self.scheduler.unlimited_queue.append(task)
                self.scheduler.feed()
                assigned_machine = self.scheduler.schedule()
                num = 1

            elif event.event_type == EventTypes.DEFERRED:
                self.scheduler.feed()
                num = 2
                assigned_machine = self.scheduler.schedule()
                if assigned_machine == -1:
                    break



            elif event.event_type == EventTypes.COMPLETION:
                # if self.verbosity <= 1:
                #     pbar.update(1)
                machine = task.assigned_machine
                machine.terminate(task)
                self.scheduler.feed()


                assigned_machine = self.scheduler.schedule()

            elif event.event_type == EventTypes.OFFLOADED:
                # if self.verbosity <= 1:
                #     pbar.update(1)
                Config.cloud.terminate(task)
                self.scheduler.feed()
                num = 4
                assigned_machine = self.scheduler.schedule()

            elif event.event_type == EventTypes.DROPPED_RUNNING_TASK:

                # if self.verbosity <= 1:
                #     pbar.update(1)
                machine = task.assigned_machine

                machine.drop()
                self.scheduler.feed()
                num = 5
                assigned_machine = self.scheduler.schedule()
            
            if Config.gui:
                self.gui1.add_task(num, task)

        # if self.verbosity <= 1:
        #     pbar.close()

        if self.scheduling_method == 'TabRLS':
            self.scheduler.done = True
        if Config.gui == 1:
            self.gui1.begin()



    def report(self, path_to_report):

        detailed_header = [

            'id', 'type', 'size', 'urgency','status','assigned_machine',
            'arrival_time','execution_time','start_time', 'completion_time',
            'deadline','extended_deadline']


        with open(path_to_report+'detailed-'+str(self.id)+'.csv','w') as results:

            detailed_writer = csv.writer(results)
            detailed_writer.writerow(detailed_header)

            for task in self.tasks:
                if task.assigned_machine == None:
                    assigned_machine = None
                else:
                    assigned_machine = task.assigned_machine.type.name
                row = [
                    task.id, task.type.name, task.task_size, task.urgency.name,
                    task.status.name, assigned_machine, task.arrival_time,
                    task.execution_time, task.start_time, task.completion_time,
                    task.deadline, task.deadline + task.devaluation_window
                ]
                detailed_writer.writerow(row)

        total_assigned_tasks = 0
        total_completion = 0
        total_xcompletion = 0
        missed_urg = 0
        missed_be = 0

        s = 'Scheduler Summary:\n\tTotal# of Tasks: {:}\n\t#Mapped: {:}\n\t#Cancelled: {:}\n\t#Offloaded: {:}\n\tDeferred: {:}'.format(
            self.total_no_of_tasks, len(self.scheduler.stats['mapped']),
            len(self.scheduler.stats['dropped']), len(self.scheduler.stats['offloaded']),
            len(self.scheduler.stats['deferred'])
        )



        if self.verbosity == 1:
            print(s)
        Config.log.write(s)

        for machine in Config.machines:
            total_assigned_tasks += machine.stats['assigned_tasks']
            total_completion += machine.stats['completed_tasks']
            total_xcompletion += machine.stats['xcompleted_tasks']
            missed_urg += machine.stats['missed_URG_tasks']
            missed_be += machine.stats['missed_BE_tasks']
            completed_percent = 0
            xcompleted_percent = 0
            energy_percent = 0
            if machine.stats['assigned_tasks'] != 0:
                completed_percent = machine.stats['completed_tasks'] / machine.stats['assigned_tasks']
                xcompleted_percent = machine.stats['xcompleted_tasks'] / machine.stats['assigned_tasks']
                energy_percent = machine.stats['energy_usage'] / Config.total_energy

            s = '\nMachine: {:} (id#{:})  \n\t%Completion: {:2.1f} #: {:}\n\t%XCompletion:{:2.1f} #: {:}\n\t#Missed URG:{:1.2f}\n\tMissed BE:{:}\n\t%Energy: {:2.1f} '.format(
                machine.type.name,machine.id,
                100*completed_percent, machine.stats['completed_tasks'],
                100*xcompleted_percent, machine.stats['xcompleted_tasks'],
                machine.stats['missed_URG_tasks'],
                machine.stats['missed_BE_tasks'],
                100*energy_percent)
            if self.verbosity <= 3 :
                print(s)
            Config.log.write(s)


        no_of_offloaded_tasks = Config.cloud.stats['offloaded_tasks']
        total_completion += Config.cloud.stats['completed_tasks']
        total_xcompletion += Config.cloud.stats['xcompleted_tasks']
        if no_of_offloaded_tasks != 0:
            percentage_offloaded_completed = 100 * Config.cloud.stats['completed_tasks'] / Config.cloud.stats[
                'offloaded_tasks']
            percentage_offloaded_xcompleted = 100 * Config.cloud.stats['xcompleted_tasks'] / Config.cloud.stats[
                'offloaded_tasks']
        else:
            percentage_offloaded_completed = 0
            percentage_offloaded_xcompleted = 0

        s = '\n Cloud:   \n\t#offloaded:{:}\n\t%Completion: {:2.1f}\n\t%XComplettion:{:2.1f}\n\t#Missed-URG:{:},\n\t#Missed-BE:{:}'.format(
            Config.cloud.stats['offloaded_tasks'],
            percentage_offloaded_completed,
            percentage_offloaded_xcompleted,
            Config.cloud.stats['missed_URG_tasks'], Config.cloud.stats['missed_BE_tasks']
        )
        if self.verbosity <=3 :
            print(s)

        Config.log.write(s)
        total_completion_percent = 100 * (total_completion / self.total_no_of_tasks)
        total_xcompletion_percent = 100 * (total_xcompletion / self.total_no_of_tasks)
        s = '\n%Total Completion: {:2.1f}'.format(total_completion_percent)
        s += '\n%Total xCompletion: {:2.1f}'.format(total_xcompletion_percent)
        s += '\n%deferred: {:2.1f}'.format(len(self.scheduler.stats['deferred']))
        s += '\n%dropped: {:2.1f}'.format(len(self.scheduler.stats['dropped']))
        s += '\n%offloaded: {:2.1f}'.format(len(self.scheduler.stats['offloaded']))

        if self.scheduling_method == 'TabRLS':
            s += '\n\tTotal Reward:{}\n\tAverage Reward:{}'.format(np.sum(self.scheduler.rewards),
            np.mean(self.scheduler.rewards))

        if self.verbosity <= 3:
            print(s)
        Config.log.write(s)

        
        d = {}
        for task_type in Config.task_types:
            #d = {}
            for machine_type in Config.machine_types:
                d [task_type.name+'_assigned_to_'+machine_type.name] = 0
                d[task_type.name+'_completed_'+machine_type.name]=0
                d[task_type.name+'_xcompleted_'+machine_type.name] = 0
                d[task_type.name+'_missed_'+machine_type.name]=0
            #task_report[task_type.name] = d
        
                            

        for task in self.tasks:

            if task.assigned_machine != None:
                d[task.type.name+'_assigned_to_'+task.assigned_machine.type.name] +=1

                if task.status.name == 'COMPLETED':
                    d[task.type.name+'_completed_'+task.assigned_machine.type.name] +=1
                elif task.status.name == 'XCOMPLETED':
                    d[task.type.name+'_xcompleted_'+task.assigned_machine.type.name] +=1
                elif task.status.name == 'MISSED':
                    d[task.type.name+'_missed_'+task.assigned_machine.type.name] +=1

        task_report = pd.DataFrame(d, index= [self.id])

        # for task_type in Config.task_types:
        #     for machine_type in Config.machine_types:
        #         total_assigned = task_report[task_type.name+'_assigned_to_'+machine_type.name].values[0]
        #         task_report[task_type.name+'_assigned_to_'+machine_type.name] /= (0.01*self.total_no_of_tasks)
        #         if total_assigned != 0 :
        #             task_report[task_type.name+'_completed_'+machine_type.name] /= (0.01*total_assigned)
        #             task_report[task_type.name+'_xcompleted_'+machine_type.name] /= (0.01*total_assigned)
        #             task_report[task_type.name+'_missed_'+machine_type.name] /= (0.01*total_assigned)
        task_report /= (0.01*self.total_no_of_tasks)
        task_report = task_report.round(2)

        
        
        row = []
        row.append(
            [self.id,self.total_no_of_tasks ,
            total_assigned_tasks, Config.cloud.stats['offloaded_tasks'],
            len(self.scheduler.stats['dropped']),
            total_completion_percent, total_xcompletion_percent,
            total_completion_percent+total_xcompletion_percent,
            missed_urg,
            missed_be,
            100* (1 - (Config.available_energy / Config.total_energy)) ])
        
        return row, task_report
