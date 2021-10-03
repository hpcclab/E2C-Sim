#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 19:53:31 2021

@author: Ali Mokhtari
"""

import numpy as np
import seaborn as sns
from scipy import stats
import csv



path = '../data/execution_times/'
task_type = 1
machine_type = 't2xlarge'

dis = []
with open(path+str(task_type)+'-'+machine_type+'.csv','r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:            
        dis.append(float(row[0]))

stat = stats.describe(dis)
print(stat[2], np.sqrt(stat[3]))
norm_dis = np.random.normal(stat[2],0.01 , stat[0] )
norm_stat = stats.describe(norm_dis)
print(norm_stat)
        
sns.displot([dis,norm_dis], fill=True)

