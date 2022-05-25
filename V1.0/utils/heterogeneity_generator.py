#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 00:14:57 2022

@author: c00424072
"""

import pandas as pd
import numpy as np 
from heterogeneity_level import *



execution_times = [100,100 ,100,100,10,1]
tasks = ['T0', 'T1', 'T2', 'T3']
machines = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7']

no_samples = 100


no_tasks = len(tasks)
no_machines = len(machines)
etc = np.zeros((no_tasks, no_machines))
H_indices = pd.DataFrame(columns = ['etc_id', 'H_index', 'n_clusters'])

for sample in range(no_samples):
    
    rnd_et = np.random.choice(execution_times, size = etc.shape[1])
    epsilon = np.random.random(size = etc.shape)
    
    for i in range(no_tasks):
        for j in range(no_machines):
            noise = np.random            
            etc[i,j] = (1+0.1*epsilon[i,j])*rnd_et[j]
    df = pd.DataFrame(data = etc, columns = machines, index = tasks)    
    df.to_csv(f'../workload/execution_times/etc/etc-het-{sample}.csv')
    
    
    h_index, n_clusters,_,_,_ = heterogeneity_level(sample, saved=True)
    print(f'etc#: {sample}  h_index:{h_index}')
    
    d = {'etc_id': sample,
         'H_index':h_index,
         'n_clusters': n_clusters}
    H_indices = H_indices.append(d, ignore_index = True)
H_indices.to_csv('etc_hindex.csv', index = False)
    


