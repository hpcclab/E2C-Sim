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
    


schedulers = ['FEE','EE','MM','MMU']
objective = 'energy_per_completion'

task_hete = 0

df_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'totalCompletion%',
                                                'energy_per_completion%',
                                                'consumed_energy%','wasted_energy%', 'CI_energy_per_completion'])
#df_summary['energy_per_completion'] = 1000.0 * df_summary['energy_per_completion']

hatch = ['///','\\\\\\']
colors = ['navy','darkred','orange', 'purple']
markers = ['o','x','s','+']


for scheduler in schedulers:
        
    for rate in [0,2,3,4,5,6,7,8]:
    
        workload = f'{rate}-{task_hete}'
        path = f'../../output/data/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path)      
        d = df.mean().loc[['totalCompletion%','consumed_energy%','wasted_energy%','energy_per_completion%']]     
        d['rate-id'] = int(rate)        
        d['scheduler'] = scheduler
        # d['CI_energy_per_completion'] = mean_confidence_interval(df['energy_per_completion%'])
        # d['CI_wasted_energy'] = mean_confidence_interval(df['wasted_energy%'])        
        # d['CI_consumed_energy'] = mean_confidence_interval(df['consumed_energy%'])
        d[f'CI_{objective}'] = mean_confidence_interval(df[f'{objective}%'])
        df_summary = df_summary.append(d, ignore_index=True)
        df_summary['rate-id'] = df_summary['rate-id'].astype('int')
        

    
x = df_summary[df_summary['scheduler']==scheduler]['rate-id'].values

width = 1.5
dist = 1.0



#rate_label = [round(2000/x,1) for x in [1000, 800, 667, 500, 400, 333, 250, 200, 100,20]]
rate_label = [round(2000/x,1) for x in [1000, 667, 500, 400, 333, 250, 200, 100]]

r0 = 0
r = [(r0-0.5*width+i*(2*width+dist)) for i in range(8)]
i = 0
plt.figure()
for scheduler in schedulers:
    if scheduler == 'EE':
        label = 'ELARE'
    elif scheduler == 'FEE':
        label = 'FELARE'
    else:
        label = scheduler
    
    #r = [r[k] + i*width for k in range(len(r))]    
    r = [r[k] for k in range(len(r))]    
    # y = df_summary[df_summary['scheduler']==scheduler]['energy_per_completion%'].values
    # y = df_summary[df_summary['scheduler']==scheduler]['wasted_energy%'].values
    # y = df_summary[df_summary['scheduler']==scheduler]['consumed_energy%'].values
    
    
    # yerr = df_summary[df_summary['scheduler']==scheduler]['CI_energy_per_completion'].values
    # yerr = df_summary[df_summary['scheduler']==scheduler]['CI_wasted_energy'].values
    # yerr = df_summary[df_summary['scheduler']==scheduler]['CI_consumed_energy'].values
    
    y = df_summary[df_summary['scheduler']==scheduler][f'{objective}%'].values
    yerr = df_summary[df_summary['scheduler']==scheduler][f'CI_{objective}'].values
    
    
    
    # plt.bar(r,y, width= width,color='none',zorder=0,
    #         hatch = hatch[i],edgecolor=colors[i],label=scheduler)
    # plt.bar(r,y, width= width, color='none',zorder=1,
    #         edgecolor='k')
    # plt.errorbar(r, y, yerr=yerr,
    #             fmt='none', c='black', capsize= 4)
    
    plt.errorbar(rate_label, y, yerr=yerr,linestyle = '--',
                fmt=markers[i],markersize=8, c=colors[i], capsize= 4, label=label)
    # plt.plot(rate_label, y, linestyle = '--',
    #             marker=markers[i], c=colors[i], label=scheduler)
    
    
    i+=1
r = [r[k] - (i-1)*width+0.5*width for k in range(len(r))]


#current_values = plt.gca().get_yticks()
# using format string '{:.0f}' here but you can choose others
#plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in current_values])
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

plt.xlabel('arrival rate [#tasks/second]', fontsize = 13)

#plt.ylabel(r'%energy per completion', fontsize=13)
# plt.ylabel(r'%consumed energy', fontsize=13)
if objective == 'wasted_energy':
    plt.ylabel(r'%wasted energy', fontsize=13)
elif objective =='consumed_energy':
    plt.ylabel(r'%consumed energy', fontsize=13)
elif objective == 'energy_per_completion':
    plt.ylabel(r'%energy per completion', fontsize=13)
    
plt.xticks(range(2,21,2))
plt.xlim(1.5, 20.5)
plt.legend()
#plt.grid(axis='y')
plt.tight_layout()
plt.savefig(f'../../output/figures/revised_with_more_arrivals/{objective}-lineplot-more-heuristics.pdf',dpi=300)
    

