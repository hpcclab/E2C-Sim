"""
Authors: Ali Mokhtari
Created on Jan. 01, 2021.

Here, The pre-defined scenarios are first read from a text file. Then, the
arrival times of tasks are written to the output file. 
Also, the output file  includes the expected and real execution time of each
task on all machine types. These values is generated using ReadData class.

** The generated output file is sorted based on the values of the arrival times.

"""

import  pandas as pd
import numpy as np
import os

from workload.random_sample import RandomSample
from workload.execution_time import ExecutionTime
import utils.config as config




class Workload:
    # The Workload class read scenarios from the file in path_to_scenarios.
    # Then, the arrival times of tasks and their task types are written to
    # "ArrivalTimes.txt" located in path_to_output.     

    
    def __init__(self, name):
        self.name = name
        self.path_to_workload = f"./workload/workloads/{self.name}"
        os.makedirs(self.path_to_workload, exist_ok = True)

        columns = ['task_type', 'arrival_time']
        for machine_type in config.machine_types:            
            columns.append(f'est_{machine_type.name}')
        
        for machine_type in config.machine_types:
            for r in range(1,machine_type.replicas+1):
                column = f'ext_{machine_type.name}-{r}'
                columns.append(column)
                                   
        self.workload = pd.DataFrame(columns = columns)
    
    def reset(self):
        columns = ['task_type', 'arrival_time']
        for machine_type in config.machine_types:            
            columns.append(f'est_{machine_type.name}')
        
        for machine_type in config.machine_types:
            for r in range(1,machine_type.replicas+1):
                column = f'ext_{machine_type.name}-{r}'
                columns.append(column)
                                   
        self.workload = pd.DataFrame(columns = columns)
        
   
    def generate(self, scenario_subname, etc_name, workload_id, seed = 100, precision=2):
        path_to_sc = f"./workload/scenarios/{self.name}/{scenario_subname}.csv"
        
        scenario = pd.read_csv(path_to_sc)
        count = 0
        
        for idx , row in scenario.iterrows():                                
            task_type = row[0]
            start_time = row[1]
            end_time = row[2]
            dist = row[3]
            no_of_tasks = row[4]
            seed = seed + 10 * int(idx)

            sample = RandomSample(start_time, end_time, no_of_tasks, seed).generate(dist)
            arrival_time = pd.DataFrame(data = sample, columns = ['arrival_time'])            
            arrival_time.insert(0,'task_type', task_type)
            if count >0:
                last_index = self.workload.index[-1]
            else:
                last_index = -1
            
            self.workload = self.workload.append(arrival_time, ignore_index=True)
            
            for machine_type in config.machine_types:

                est = ExecutionTime(self.name).sample(etc_name, task_type,machine_type,no_of_tasks, precesion=precision)                                
                
                self.workload.loc[last_index+1:, f'est_{machine_type.name}'] = est
                
                for r in range(1,machine_type.replicas+1):
                    ext = ExecutionTime(self.name).sample(etc_name, task_type,machine_type,no_of_tasks, precesion=precision)                    
                    self.workload.loc[last_index+1:,f'ext_{machine_type.name}-{r}'] = ext   
            count += 1                     
                    
                        
                        

        self.workload = self.workload.sort_values(by=['arrival_time'])
        folder = f"./workload/workloads/{self.name}/{scenario_subname}/etc-{etc_name}"
        os.makedirs(folder, exist_ok = True)
        path_to_output = f"{folder}/workload-{workload_id}.csv"
        self.workload.to_csv(path_to_output, index = False)
        return self.workload











        