#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 09:48:42 2021

@author: c00424072
"""

import pandas as pd
import matplotlib.pyplot as plt



rate =3
schedulers = ['MM','EE']

hatch = ['///','\\\\\\']
colors = ['darkred','navy']

def read_data(scheduler):
    global rate
    df_summary = pd.DataFrame(data=None, columns = ['consumed_energy%','wasted_energy%'])
    for task_hete in range(1,4):    
        workload = f'{rate}-{task_hete}'
        path = f'../../output/data/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path)      
        d = df.mean().loc[['consumed_energy%','wasted_energy%']] 
        d['task_hete'] = task_hete    
        df_summary = df_summary.append(d, ignore_index=True)
        
    x = df_summary['task_hete'].values
    x /= 4.0
    
    consumed = df_summary['consumed_energy%']
    wasted = df_summary['wasted_energy%']
    
    return x , consumed, wasted

d = 1.0
w = 0.5
r0 = 0

i = 0 
for scheduler in schedulers:
    x , consumed, wasted = read_data(scheduler)
    r = [r0-0.5*w+ k*(d + 2*w)+i*w for k in range(len(x))]
    
    plt.bar(r,wasted,width = w,hatch = hatch[i], color = 'none',
            edgecolor=colors[i] ,label = f'{scheduler}-wasted')
    plt.bar(r,wasted,width = w,color = 'none',
            edgecolor='k')
    i+=1
    
r = [r[k] - 0.5*w for k in range(len(r))]   
xlabels =  ['1/3','1','3']
plt.xticks(r,xlabels , fontsize = 14) 

plt.xlabel(r'$TT_2$ / $TT_1$', fontsize = 15)   

plt.ylabel('%energy usage', fontsize = 15)
plt.yticks(fontsize = 14)
plt.legend()
plt.tight_layout()
#plt.savefig(f'../../output/figures/task_hete_consumed_vs_wasted_{rate}.pdf',dpi=300)
plt.show()
    

