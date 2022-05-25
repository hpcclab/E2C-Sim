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
import os

from utils.random_sample import RandomSample
import utils.config as config
from utils.execution_time import ExecutionTime




class Workload:
    # The Workload class read scenarios from the file in path_to_scenarios.
    # Then, the arrival times of tasks and their task types are written to
    # "ArrivalTimes.txt" located in path_to_output.     

    #def __init__(self, het_level,consistency_level,workload_id):
    def __init__(self, het_id,workload_id):
        #self.h = het_level
        #self.a = consistency_level
        self.h = het_id
        self.workload_id = workload_id
        columns = ['task_type_id', 'arrival_time']
        for machine_type in config.machine_types:            
            columns.append(f'est_{machine_type.name}')
        
        for machine_type in config.machine_types:
            for r in range(1,machine_type.replicas+1):
                column = f'ext_{machine_type.name}-{r}'
                columns.append(column)
                           
        self.workload = pd.DataFrame(columns = columns)
   
    def generate(self, workload_no):
        path_to_sc = f"{config.settings['path_to_workload']}/scenarios/scenario-{self.workload_id}.csv"
        scenario = pd.read_csv(path_to_sc)

        count = 0
        for _ , row in scenario.iterrows():
                                 
            task_type_id = row[0]
            start_time = row[1]
            end_time = row[2]
            dist = row[3]
            no_of_tasks = row[4]
            sample = RandomSample(start_time, end_time, no_of_tasks).generate(dist)
            arrival_time = pd.DataFrame(data = sample, columns = ['arrival_time'])
            arrival_time.insert(0,'task_type_id', task_type_id)
            if count >0:
                last_index = self.workload.index[-1]
            else:
                last_index = -1
            
            self.workload = self.workload.append(arrival_time, ignore_index=True)
            
            for machine_type in config.machine_types:

                est = ExecutionTime(self.h).sample(task_type_id,machine_type,no_of_tasks)
                #print(len(est), self.workload.shape)
                self.workload.loc[last_index+1:, f'est_{machine_type.name}'] = est
                for r in range(1,machine_type.replicas+1):
                    ext = ExecutionTime(self.h).sample(task_type_id,machine_type,no_of_tasks)                    
                    self.workload.loc[last_index+1:,f'ext_{machine_type.name}-{r}'] = ext   
            count += 1                     
                    
                        
                        

        self.workload = self.workload.sort_values(by=['arrival_time'])
        # folder = f"{config.settings['path_to_workload']}/workloads/H-{self.h}-a-{self.a}/workload-{self.workload_id}"
        folder = f"{config.settings['path_to_workload']}/workloads/H-{self.h}/workload-{self.workload_id}"
        # folder = f"{config.settings['path_to_workload']}/workloads/workload-{self.workload_id}"
        os.makedirs(folder, exist_ok = True)
        path_to_output = f"{folder}/workload-{workload_no}.csv"
        self.workload.to_csv(path_to_output, index = False)
        return self.workload











        