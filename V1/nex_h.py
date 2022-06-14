#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:53:27 2022

@author: c00424072
"""

import pandas as pd
from workload.hindex import HINDEX
import os

workload_name = 'heterogeneous'
# etc_id = 0

# df = pd.read_csv(f'./etcs/{workload_name}/{etc_id}.csv',index_col = ['Unnamed: 0'])
path_to_etcs = f"./workload/etcs/{workload_name}"
etc_files = os.listdir(path_to_etcs)
if   'hindices.csv' in etc_files:
    etc_files.remove('hindices.csv')  
hidx = HINDEX(workload_name)
h_indices = pd.DataFrame(columns=['etc_id', 'h_index'])
for etc_file in etc_files:
    etc_id = etc_file.split('.')[0]
    h = hidx.hindex(etc_id, saved=True)
    h = round(h, 2) 
    #speedup = round(speedup,2)       
    d = {'etc_id': etc_id,
        'h_index':h,
        
        }
    h_indices = h_indices.append(d, ignore_index = True)
h_indices.to_csv(f'{path_to_etcs}/hindices.csv', index = False)
