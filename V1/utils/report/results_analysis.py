#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 08:41:05 2021

@author: c00424072
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

results  = pd.DataFrame(data = None, columns = ['1-low-MM', 
                                           '1-low-TabRLS',
                                           '1-medium-MM',
                                           '1-medium-TabRLS',
                                           '1-high-MM',
                                           '1-high-TabRLS',
                                           '2-low-MM', 
                                           '2-low-TabRLS',
                                           '2-medium-MM',
                                           '2-medium-TabRLS',
                                           '2-high-MM',
                                           '2-high-TabRLS'])

for i in range(1,3):
    
    path_to_oversubscription = './results/oversubscription-'+str(i)+'/'
    
    for variance in ['low','medium','high']:
        path_to_variance = path_to_oversubscription +variance+'-variance/'
        
        for scheduling_method in ['MM','TabRLS']:
            
            path_to_result = path_to_variance + scheduling_method +'/'
            
            df = pd.read_csv(path_to_result+'results-summary.csv')
            df['total_completion'] = df['Completion%'] + df['xCompletion%']
            mean = df['total_completion'].mean()
            std = df['total_completion'].std()
            
            results.loc['mean',str(i)+'-'+variance+'-'+scheduling_method] = round(mean,2)
            results.loc['std',str(i)+'-'+variance+'-'+scheduling_method] = std



x0 = 1
w = 0.3
d = 2
x = []

c = ['red', 'deepskyblue', 'brown','royalblue', 'darkred', 'navy' ]
hatch = ['///', '\\\\', '++', 'xx', '..', 'o']

labels = ['Low', 'Medium', 'High']
# for i in range(3):
#     x.append(x0+ i * d - 0.5* w)
#     x.append(x0+ i * d + 0.5* w)


fig, ax = plt.subplots()
x = np.arange(len(labels))
MM = ax.bar(x - w/2, results.iloc[0,6:12:2].values, width = w,
            hatch ='////' ,label='MM')
TabRLS = ax.bar(x + w/2, results.iloc[0,7:12:2].values, width = w,
                hatch='\\\\',label='TabRLS')

ax.set_ylabel('%Completion')
ax.set_ylim(0,100)
ax.set_title('Task Completion for Task Arrival Rate 10 tasks/sec')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(MM, padding=1)
ax.bar_label(TabRLS, padding=1)

fig.tight_layout()
plt.savefig('./highArrivalRate.jpeg')

plt.show()

                