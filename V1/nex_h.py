#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:53:27 2022

@author: c00424072
"""

import pandas as pd
from utils.hindex import HINDEX
import os

workload_name = 'heterogeneous'
# etc_id = 0

# df = pd.read_csv(f'./etcs/{workload_name}/{etc_id}.csv',index_col = ['Unnamed: 0'])
path_to_etcs = f"./task_machine_performance/heterogeneous/1_75"
etc_files = os.listdir(path_to_etcs)
if   'hindices.csv' in etc_files:
    etc_files.remove('hindices.csv') 
etc_files.remove('execution_times.csv') 
hidx = HINDEX(path_to_etcs)
h_indices = pd.DataFrame(columns=['etc_id', 'SEP'])
for etc_file in etc_files:
    etc_id = etc_file.split('.')[0]
    sep = hidx.hindex(etc_id, saved=True)
    sep = round(sep, 2) 
    print(etc_id, sep)
    #speedup = round(speedup,2)       
    d = {'etc_id': etc_id,
        'SEP':sep,
        
        }
    h_indices = h_indices.append(d, ignore_index = True)
h_indices.to_csv(f'{path_to_etcs}/hindices.csv', index = False)
