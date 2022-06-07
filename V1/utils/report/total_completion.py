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

df_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'totalCompletion%'])

yerr_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'totalCompletion%'])

hatch = [['++','\\\\\\'],['///', 'xxx']]
#colors = [['seagreen','darkorange'],['salmon','darkcyan']]
#colors = [['seagreen','darkslateblue'],['salmon','darkcyan']]

colors = ['navy','darkred']
markers = ['o','x']

objective = ['total_completion']

for scheduler in schedulers:
        
    for rate in [0,2,3,4,5,6,7,8]:
    
        workload = f'{rate}-{task_hete}'
        path = f'../../output/data/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path, usecols=['totalCompletion%'])        
        
        
        d = df.mean().loc[['totalCompletion%']]        
        d['rate-id'] = int(rate)        
        d['scheduler'] = scheduler
        
        yerr = mean_confidence_interval(df['totalCompletion%'].values)
        
        d_err = {'totalCompletion%':yerr,
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
rate_label = [round(2000/x,1) for x in [1000,  667, 500, 400, 333, 250, 200, 100]]

r = [(r0-0.5*width+i*(2*width+dist)) for i in range(9)]

i = 0
plt.figure()

fig = plt.figure()
ax1 = fig.add_subplot(111)
for scheduler in schedulers:    
    r = [r[k] + 0*width for k in range(len(r))]    
    y = df_summary[df_summary['scheduler']==scheduler]['totalCompletion%'].values
    
    
    yerr = yerr_summary[df_summary['scheduler']==scheduler]['totalCompletion%'].values
    
    
    #y1 /= 20
    #y2 /= 20
    
   

    
    # ax1.bar(r,y, width= width, color='none',zorder=0,
    #         hatch = hatch[i][0],edgecolor=colors[i][0],label=f'{scheduler}-missed')
    
    # ax1.bar(r,y, width= width, color='none',zorder=1,edgecolor='k')
    
   
    plt.errorbar(rate_label, y, yerr=yerr,linestyle = '--',
                fmt=markers[i], c=colors[i], capsize= 4, label=scheduler)
    
    
    i+=1
r = [r[k] - (i-1)*width+0.5*width for k in range(len(r))]

plt.xlabel('arrival rate [#tasks/second]', fontsize = 14)
#plt.ylabel('% Consumed Energy')
plt.ylabel(r'%total completion', fontsize = 14)
plt.xticks(range(2,21,2))
plt.xlim(1.5, 20.5)
plt.legend()
#plt.grid(axis='y')
plt.tight_layout()
plt.savefig(f'../../output/figures/revised_with_more_arrivals/total_completion_revised.pdf',dpi=300)
    

