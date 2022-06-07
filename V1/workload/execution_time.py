"""
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

Description:

"""
# from etc_generator import gamma
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import makedirs

class ExecutionTime:
    # Here, the execution time of task type on a specific machine type
    # is read from the dataset. Then, an execution time is sampled and
    # return as estimated or real execution time. 

    def __init__(self, name):        
        self.execution_times = None
        self.name = name
        
    def sample(self, etc_name, task_type_id, machine_type, size, precesion=3):
        # Here, the execution time of task type on a specific machine type
        # is read from the dataset. This function returns a list that 
        # contains the execution times.
        # the file name of the dataset must be in the format of 
        # <task_type_id>-<machine_type>.csv (e.g. 1-CPU.csv)
            
        path_to_file =f"./workload/execution_times/{self.name}/{etc_name}/{task_type_id}-{machine_type.name}.csv"
        data = pd.read_csv(path_to_file)
        self.execution_times = np.random.choice(data['execution_time'].values, size)
        self.execution_times = [round(x, precesion) for x in self.execution_times]    
        
        return self.execution_times
    
    def synthesize(self, etc_name, task_type, machine_type,variance, size):
        path_to_etc =  f'./workload/etcs/{self.name}/{etc_name}.csv'       
        etc = pd.read_csv(path_to_etc)
        etc = etc.rename(columns={'Unnamed: 0':'task_types'})
        etc = etc.set_index('task_types')

        etc_ij = etc.loc[f'{task_type}',f'{machine_type}']
        low = etc_ij*(1-variance*np.sqrt(3))
        high = 2*etc_ij - low
        
        self.execution_times = np.random.uniform(low, high, size)        
        self.execution_times = [round(x, 3) for x in self.execution_times]
        df = pd.DataFrame(data=self.execution_times, columns=['execution_time'])
        path_to_result = f'./workload/execution_times/{self.name}/{etc_name}'
        makedirs(path_to_result, exist_ok = True)
        df.to_csv(f'{path_to_result}/{task_type}-{machine_type}.csv', index= False)

        return self.execution_times