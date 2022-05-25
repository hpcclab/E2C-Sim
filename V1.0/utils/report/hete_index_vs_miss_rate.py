#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 02:47:48 2022

@author: c00424072
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np

    


# schedulers = ['FEE','EE','MM','MMU','MSD']
schedulers = ['EE']

df_summary = pd.DataFrame(data=None, columns = ['sample','het-idx','scheduler' ,'totalCompletion%', 'consumed_energy%'])


path_h_indices = f'../../workload/execution_times/etc/etc_hindex.csv'

df_h = pd.read_csv(path_h_indices)
#df_h = df_h.sort_values(by='H_index')
het_indices = df_h['H_index'].values
df_summary['het-idx'] = het_indices
df_summary['sample'] = df_h['etc_id'].values




objective = 'totalCompletion%'

for scheduler in schedulers:
        
    for h in range(100):
             
        workload = '3-0'
        path = f'../../output/data/H-het-{h}/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path, usecols= [objective])              
        df_summary.loc[df_summary['sample']==h, ['scheduler', objective]] = [ scheduler, df.mean().loc[[objective]].values]
        
        
   

colors = ['navy','darkred','orange', 'purple','darkgreen']
markers = ['o','x','<','+','s']



plt.figure()
i=0

for scheduler in schedulers:
    
    results = df_summary[df_summary['scheduler']==scheduler]
    results = results.sort_values('het-idx')
    
    if scheduler == 'EE':
        label = 'ELARE'
    elif scheduler == 'FEE':
        label = 'FELARE'
    else:
        label = scheduler    
    
    total_completion = results['totalCompletion%'].values
    het_ids = results['het-idx'].values    
    plt.plot(het_ids, 100-total_completion, 
             marker = markers[i],
             color= colors[i],
             #linestyle='-',
            label = label)
    
    
    # if scheduler == 'EE':
    #     plt.fill_betweenx(100-total_completion,consumed_energy, x2=100,color= 'lightgrey',
    #                       alpha=0.5, interpolate=True)
    #     bbox = dict(boxstyle ="round", fc ="white", color = 'k',pad=0.5)
    #     plt.annotate('dominated solutions',
    #                     xy = (80,60), xytext =(70,80),color='k',
    #                     #textcoords ='offset points',
    #                     bbox = bbox,horizontalalignment='center',fontsize=12) 
        
    #     bbox = dict(boxstyle ="round", fc ="none", color='k')
    #     arrowprops = dict(
    #         arrowstyle = "->", lw = 1.3,
    #         connectionstyle = "angle, angleA = 0, angleB = 90,\
    #         rad = 10",
    #         )
        
            
        
# =============================================================================
#         for _, row in results.iterrows():
#             rate = row['rate-id']
#             loc = row[['consumed_energy%','totalCompletion%']].values
#             loc[1] = 100 - loc[1]
#             
#             
#             print(i, rate)
#             
#             if i==1 and rate == 3:
#                 
#                 xdata, ydata = loc[0], loc[1]
#                 #xdisplay, ydisplay = plt.transData.transform((xdata, ydata))
#                   
#                 bbox = dict(boxstyle ="round", fc ="none", color='k', pad=0.6)
#                 arrowprops = dict(
#                     arrowstyle = "->", lw = 1.3,color='k',
#                     connectionstyle = "angle, angleA = 0, angleB = 90,\
#                     rad = 10",
#                     )
#                   
#                 offset = -20
#                 
#                 # Annotation
#                 plt.annotate('Pareto front',
#                             xy = (xdata-2, ydata+2), xytext =(20,20),color='k',
#                             #textcoords ='offset points',
#                             bbox = bbox, arrowprops = arrowprops, rotation = 0,
#                             horizontalalignment='center',fontsize=12) 
#             
#             # plt.annotate('arrival rate < %.1f'%(rate_label[rate]),
#             #             xy = (30,30), xytext =(35,30),
#             #             #textcoords ='offset points',
#             #             bbox = bbox, rotation = -30) 
#             
#             # plt.annotate('arrival rate > %.1f'%(rate_label[rate]),
#             #             xy = (30,30), xytext =(5,65),
#             #             #textcoords ='offset points',
#             #             bbox = bbox, rotation = -25) 
#             
#             #plt.annotate(str(rate_label[rate]), loc)
#         #plt.annotate('arrival rates',[30,30])
# =============================================================================
    i+=1


plt.xlabel('H-index', fontsize= 14)
plt.ylabel('%unsuccessful tasks', fontsize= 14)
#plt.xlim(0,100)
#plt.ylim(0,100)
# plt.legend(loc=(0.78,0.1))
plt.legend()
plt.tight_layout()
#plt.savefig(f'../../output/figures/missrate_vs_h_index.pdf',dpi=300)
   


