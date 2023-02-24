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

    def __init__(self, seed):        
        self.execution_time = None        
        self.seed = seed

    def synthesize(self, etc, task_type, machine_type,variance):
        np.random.seed(self.seed)        
        etc_ij = etc.loc[f'{task_type}',f'{machine_type}']
        low = etc_ij*(1-variance*np.sqrt(3))
        high = 2*etc_ij - low        
        self.execution_time = np.random.uniform(low, high)        
        self.execution_time = round(self.execution_time, 3)

        return self.execution_time