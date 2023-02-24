#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 09:48:42 2021

@author: c00424072
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np




schedulers = ['MM','EE']
rate =8
task_hete =0

df_summary = pd.DataFrame(data=None, columns = ['scheduler' ,                                                
                                                'consumed_energy%','wasted_energy%'])
#df_summary['energy_per_completion'] = 1000.0 * df_summary['energy_per_completion']

hatch = ['///','\\\\\\']
colors = ['navy','darkred']


for scheduler in schedulers:    
    workload = f'{rate}-{task_hete}'
    path = f'../../output/data/{workload}/{scheduler}/results-summary.csv'
    df = pd.read_csv(path)      
    d = df.mean().loc[['consumed_energy%','wasted_energy%']] 
    d['scheduler'] = scheduler    
    df_summary = df_summary.append(d, ignore_index=True)
    
    
x = df_summary[df_summary['scheduler']==scheduler].values

width = 1.5
dist = 1.0
labels = ['total', 'wasted']

r0 = 0
r = [(r0-0.5*width+i*(2*width+dist)) for i in range(len(schedulers))]
i = 0
plt.figure()
for scheduler in schedulers:
    k = 0
    for obj in ['consumed_energy%','wasted_energy%']:
        x = r[i] +  k*width  
        y = df_summary[df_summary['scheduler']==scheduler][obj].values
        
         
        
        if i==0:
            plt.bar(x,y, width= width,color='none',zorder=0,
                    hatch = hatch[k],edgecolor=colors[k],label=labels[k])
        else:
             plt.bar(x,y, width= width,color='none',zorder=0,
                    hatch = hatch[k],edgecolor=colors[k])
             
        plt.bar(x,y, width= width, color='none',zorder=1,
                edgecolor='k')
        k+=1
    i+=1
r = [r[k]+0.5*width for k in range(len(r))]
plt.xticks(r,schedulers )

#current_values = plt.gca().get_yticks()
# using format string '{:.0f}' here but you can choose others
#plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in current_values])
#plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

plt.xlabel('scheduling heuristics', fontsize = 13)
#plt.ylabel('% Consumed Energy')
plt.ylabel(r'%energy usage', fontsize=13)
plt.ylim([0,49])
plt.legend(ncol=2)
#plt.grid(axis='y')
#plt.savefig(f'../../output/figures/consumed_vs_wasted_{rate}-{task_hete}.pdf',dpi=300)
    

