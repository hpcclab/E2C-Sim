#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 10:59:19 2022

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
    


schedulers = ['FEE','EE','MM','MMU','MSD']
#schedulers = ['MM','FEE']
hete = []

for i in range(100):
    s = f'het-{i}'
    hete.append(s)


task_hete = 0

df_summary = pd.DataFrame(data=None, columns = ['het-id','scheduler' ,'totalCompletion%', 'consumed_energy%'])

yerr_summary = pd.DataFrame(data=None, columns = ['het-id','scheduler' ,'totalCompletion%','consumed_energy%'])

hatch = [['++','\\\\\\'],['///', 'xxx']]
#colors = [['seagreen','darkorange'],['salmon','darkcyan']]
#colors = [['seagreen','darkslateblue'],['salmon','darkcyan']]

colors = ['navy','darkred','orange', 'purple','darkgreen']
markers = ['o','x','<','+','s']

objective = ['total_completion']

for scheduler in schedulers:
        
    for h in range(100):
        het_id = f'het-{h}'
        #workload = f'{rate}-{task_hete}'
        workload = '5-0'
        path = f'../../output/data/H-{het_id}/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path, usecols=['totalCompletion%', 'consumed_energy%'])        
        
        
        d = df.mean().loc[['totalCompletion%', 'consumed_energy%']]        
        d['het-id'] = het_id
        d['scheduler'] = scheduler
        
        yerr_compl = mean_confidence_interval(df['totalCompletion%'].values)
        yerr_energy = mean_confidence_interval(df['consumed_energy%'].values)
        
        d_err = {'totalCompletion%':yerr_compl,
                 'consumed_energy%':yerr_energy,
                'rate-id':het_id,
                'scheduler':scheduler
                        }
        yerr_summary = yerr_summary.append(d_err, ignore_index=True)
        df_summary = df_summary.append(d, ignore_index=True)
        # df_summary['rate-id'] = df_summary['rate-id'].astype('int')
    

# rate_label = [round(2000/x,1) for x in [1000, 800, 667, 500, 400, 333, 250, 200, 100,20]]

# rate_label.sort()

plt.figure()
i=0

for scheduler in schedulers:
    
    results = df_summary[df_summary['scheduler']==scheduler]
    
    if scheduler == 'EE':
        label = 'ELARE'
    elif scheduler == 'FEE':
        label = 'FELARE'
    else:
        label = scheduler
    
    consumed_energy = results['consumed_energy%'].values
    total_completion = results['totalCompletion%'].values
    het_ids = results['het-id'].values
    # plt.scatter(consumed_energy, 100-total_completion, 
    #          marker = markers[i],
    #          color= colors[i],
    #          #linestyle='-',
    #         label = label)
    plt.scatter(consumed_energy, 100-total_completion, 
             marker = markers[i],
             color= colors[i],
             #linestyle='-',
            label = label)
    #if scheduler == 'FEE':
    # for k in range(len(consumed_energy)):
    #     plt.annotate(f"{het_ids[k]}",xy =(consumed_energy[k],100-total_completion[k]) ,
    #                   xytext = (consumed_energy[k],100-total_completion[k]))
        
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


plt.xlabel('%energy consumption', fontsize= 14)
plt.ylabel('%unsuccessful tasks', fontsize= 14)
#plt.xlim(0,100)
#plt.ylim(0,100)
# plt.legend(loc=(0.78,0.1))
plt.legend()
plt.tight_layout()
#plt.savefig(f'../../output/figures/pareto_het.pdf',dpi=300)
   


