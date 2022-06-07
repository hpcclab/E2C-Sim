#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 00:14:57 2022

@author: c00424072
"""

import pandas as pd
import numpy as np 
import os

from workload.hindex import HINDEX

class ETC:

    def __init__(self,name):
        self.name = name
        self.path_to_etcs = f"./workload/etcs/{self.name}"
        os.makedirs(self.path_to_etcs, exist_ok = True)



    def generate(self, tasks, machines, et_set, no_of_samples, seed = 100):        
        no_tasks = len(tasks)
        no_machines = len(machines)
        etc = np.zeros((no_tasks, no_machines))

        for sample in range(no_of_samples):
            print(f'etc# {sample} is generated ...')
            seed = seed + 7*sample
            np.random.seed(seed)
            rnd_et = np.random.choice(et_set, size = etc.shape[1])
            epsilon = np.random.random(size = etc.shape)
            for i in range(no_tasks):
                for j in range(no_machines):                
                    etc[i,j] = (1+0.1*epsilon[i,j])*rnd_et[j]
                    etc[i,j] = round(etc[i,j],2)
            df = pd.DataFrame(data = etc, columns = machines, index = tasks)    
            df.to_csv(f'{self.path_to_etcs}/{sample}.csv')
            
            
    
    def hindices(self):
        etc_files = os.listdir(self.path_to_etcs)
        if   'hindices.csv' in etc_files:
            etc_files.remove('hindices.csv')  
        hidx = HINDEX(self.name)
        h_indices = pd.DataFrame(columns=['etc_id', 'h_index'])
        for etc_file in etc_files:
            etc_id = etc_file.split('.')[0]
            h = hidx.hindex(etc_id, saved=True)
            h = round(h, 2)        
            d = {'etc_id': etc_id,
                'h_index':h}
            h_indices = h_indices.append(d, ignore_index = True)
        h_indices.to_csv(f'{self.path_to_etcs}/hindices.csv', index = False)
            


