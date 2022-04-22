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



def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h
    


schedulers = ['EE','MM']

task_hete = 0

df_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'BE_missed',
                                                'cancelled'])

yerr_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'BE_missed',
                                                'cancelled'])

# hatch = [['...','\\\\\\'],['///', 'xxx']]
hatch = [['////','\\\\\\'],['xxx', '...']]
#colors = [['seagreen','darkorange'],['salmon','darkcyan']]
colors = [['seagreen','darkslateblue'],['salmon','darkcyan']]



objective = ['BE_missed', 'cancelled']

for scheduler in schedulers:
        
    for rate in [0,2,3,4,5,6,7,8]:
    
        workload = f'{rate}-{task_hete}'
        path = f'../../output/data/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path, usecols=['total_no_of_tasks','BE_missed','cancelled'])
        df = pd.read_csv(path, usecols=['total_no_of_tasks','BE_missed','cancelled'])
        df['BE_missed'] = 100 * df['BE_missed'] /  df['total_no_of_tasks']
        df['cancelled'] = 100 * df['cancelled'] /  df['total_no_of_tasks']
        
        
        d = df.mean().loc[['BE_missed','cancelled']]        
        d['rate-id'] = int(rate)        
        d['scheduler'] = scheduler
        
        yerr_missed = mean_confidence_interval(df['BE_missed'].values)
        yerr_cancelled = mean_confidence_interval(df['cancelled'].values)
        d_err = {'BE_missed':yerr_missed,
                 'cancelled': yerr_cancelled,
                'rate-id':rate,
                'scheduler':scheduler
                        }
        yerr_summary = yerr_summary.append(d_err, ignore_index=True)
        df_summary = df_summary.append(d, ignore_index=True)
        df_summary['rate-id'] = df_summary['rate-id'].astype('int')
    
x = df_summary[df_summary['scheduler']==scheduler]['rate-id'].values

width = 1.0
dist = 1.0
r0 = 0

#rate_label = [x for x in [1,1000/800,1.5, 1000/500, 1000/400,3 ]]
#rate_label = [round(2000/x,1) for x in [1000, 800, 667, 500, 400, 333, 250, 200, 100,20]]
rate_label = [round(2000/x) for x in [1000,  667, 500, 400, 333, 250, 200, 100]]

r = [(r0-0.5*width+i*(2*width+dist)) for i in range(8)]

i = 0
plt.figure()

fig = plt.figure()
ax1 = fig.add_subplot(111)
for scheduler in schedulers:    
    r = [r[k] + i*width for k in range(len(r))]    
    y1 = df_summary[df_summary['scheduler']==scheduler]['BE_missed'].values
    y2 = df_summary[df_summary['scheduler']==scheduler]['cancelled'].values
    
    yerr1 = yerr_summary[df_summary['scheduler']==scheduler]['BE_missed'].values
    yerr2 = yerr_summary[df_summary['scheduler']==scheduler]['cancelled'].values
    
    #y1 /= 20
    #y2 /= 20
    
    if scheduler == 'EE':
         label = 'ELARE'
    elif scheduler == 'FEE':
        label = 'FELARE'
    else:
        label = scheduler

    
    ax1.bar(r,y1, width= width, color='none',zorder=0,
            hatch = hatch[i][0],edgecolor=colors[i][0],label=f'{label}-missed')
    
    ax1.bar(r,y1, width= width, color='none',zorder=1,edgecolor='k')
    
    
    ax1.bar(r,y2, bottom=y1,width= width, color='none',zorder=0,
            hatch = hatch[i][1],edgecolor=colors[i][1],label=f'{label}-cancelled')
    
    
    
    ax1.bar(r,y2, bottom=y1,width= width, color='none',zorder=1,edgecolor='k')
    
    plt.errorbar(r, y1, yerr=yerr1,
               fmt='none', c='black',  capsize= 3)
    plt.errorbar(r, y2+y1, yerr=yerr2,
               fmt='none', c='black', capsize= 3)
    
    
    
    i+=1
r = [r[k] - (i-1)*width+0.5*width for k in range(len(r))]
plt.xticks(r,rate_label )
plt.xlabel('arrival rate [#tasks/second]', fontsize = 14)
#plt.ylabel('% Consumed Energy')
plt.ylabel(r'%unsuccessful tasks', fontsize = 14)
plt.ylim([0,105])
plt.legend(loc=[0.01,0.82],ncol=2)
#plt.grid(axis='y')
plt.tight_layout()
plt.savefig(f'../../output/figures/revised_with_more_arrivals/missed_cancelled_revised.pdf',dpi=300)
    

