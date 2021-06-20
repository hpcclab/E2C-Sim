"""
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

The real and estimated execution times of each task is generated using
this module. To that end, a dataset which contains the execution times
of each task type is used to uniformly sample a time as real or estimated
execution time. 
The dataset should contain execution times in the format of 
<task_type_id>-<machine_type>.txt

"""
import csv
import os
import numpy as np
import random

# path to the data set directory
base = '../data/execution_times/'


class ReadData:
    # Here, the execution time of task type on a specific machine type
    # is read from the dataset. Then, an execution time is sampled and
    # return as estimated or real execution time. 

    def __init__(self, data_path='../data/execution_times/',
                 output_path='./'):
        self.data_path = data_path
        self.output_path = output_path

    def read_execution_time(self, task_type_id, machine_type):
        # Here, the execution time of task type on a specific machine type
        # is read from the dataset. This function returns a list that 
        # contains the execution times.
        # the file name of the dataset must be in the format of 
        # <task_type_id>-<machine_type>.txt (e.g. 1-CPU.txt)

        execution_times = []
        file_name = str(task_type_id) + '-' + machine_type + '.txt'
        path = self.data_path + file_name
        try:
            with open(path, 'r') as data_file:
                for line in data_file:
                    execution_times.append(float(line))

            return execution_times
        finally:
            print("Error opening file.")
            pass

    def sampled_execution_times(self, task_type_id, machine_type, k=1):
        # Here, it takes task_type_id, machine_type and "k", then read the
        # execution times from the dataset and finally returns a sample of 
        # "k" execution times. 

        sampled_execution_times = []
        execution_times = self.read_execution_time(task_type_id, machine_type)

        for _ in range(k):
            sampled_execution_times.append(random.choice(execution_times))

        sampled_execution_times = [round(x, 3) for x in sampled_execution_times]

        return sampled_execution_times
