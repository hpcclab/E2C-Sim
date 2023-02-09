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


class Workload:
    # The Workload class read scenarios from the file in path_to_scenarios.
    # Then, the arrival times of tasks and their task types are written to
    # "ArrivalTimes.txt" located in path_to_output.     

    
    def __init__(self):               
        self.workload = pd.DataFrame(columns = ['task_type', 'arrival_time'])
    
    def reset(self):               
        self.workload = pd.DataFrame(columns = ['task_type', 'arrival_time'])        
   
    
    def generate(self, scenario_name, workload_id, seed = 100, precision=2):
        path_to_sc = f"./workloads/scenarios/{scenario_name}.csv"        
        scenario = pd.read_csv(path_to_sc)

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
            self.workload = self.workload.append(arrival_time, ignore_index=True)
            
        self.workload = self.workload.sort_values(by=['arrival_time'])
        folder = f"./workloads/{scenario_name}"
        os.makedirs(folder, exist_ok = True)
        path_to_output = f"{folder}/workload-{workload_id}.csv"
        self.workload.to_csv(path_to_output, index = False)
        print('here')
        return self.workload










        