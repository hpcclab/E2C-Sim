#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:36:43 2021

@author: c00424072
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

schedulers = ['FEE']
n = len(schedulers)
workload = '3-2'

task_types = ['TT1', 'TT2']
machine_types = ['m1', 'm2']

i = 0
#fig, ax = plt.figure()
fig, ax = plt.subplots()
#ax = fig.add_axes([0,0,1,1])
width = 0.15
d = 1*width
r0= 0
r = []
hatch = [['xx','xx'] ,[ 'oo', 'oo'],['\\\\','\\\\']]
colors = [['darkred', 'navy'], ['orange', 'darkgreen'],['indigo', 'lightseagreen']]

for scheduler in schedulers:
    path = f'../../output/data/{workload}/{scheduler}/task_based_report.csv'
    #path = f'/home/C00424072/Ali/Projects/smartsight/V1.0/output/data/{workload}/{scheduler}/task_based_report.csv'
    
    df = pd.read_csv(path)
    df['TT1_m1-1_total_completed'] = df['TT1_completed_m1-1'] + df['TT1_xcompleted_m1-1']
    df['TT2_m1-1_total_completed'] = df['TT2_completed_m1-1'] + df['TT2_xcompleted_m1-1']
    
   
    df['TT1_m2_total_completed'] = df['TT1_completed_m2'] + df['TT1_xcompleted_m2']
    df['TT2_m2_total_completed'] = df['TT2_completed_m2'] + df['TT2_xcompleted_m2']
    
    df['TT1_m1_total_completed'] = 0
    df['TT2_m1_total_completed'] = 0
    
    for k in range(1,5):
        df['TT1_m1_total_completed'] += df[f'TT1_m1-{k}_total_completed'] 
        df['TT2_m1_total_completed'] += df[f'TT2_m1-{k}_total_completed'] 
        
    mean_values = df.mean(axis=0)    
    
    
    # m1 = df.loc[:,['TT1_assigned_to_m1', 'TT2_assigned_to_m1']]
    # m2 = df.loc[:,['TT1_assigned_to_m2', 'TT2_assigned_to_m2']]
    
    m1 = df.loc[:,['TT1_m1_total_completed', 'TT2_m1_total_completed']]
    m2 = df.loc[:,['TT1_m2_total_completed', 'TT2_m2_total_completed']]
    
    # m11 = m11.mean(axis=0).values
    # m12 = m12.mean(axis=0).values
    # m13 = m13.mean(axis=0).values
    # m14 = m14.mean(axis=0).values
    
    m1 = m1.mean(axis=0).values    
    m2 = m2.mean(axis=0).values
    #not_assigned = [(1 - m2[0] - m1[0]), (1 - m2[1] - m1[1])]
     
        

   
    
    r.append([ r0+i*width,r0+ (n+i)*width + d]) # the x locations for the groups
    
    plt.bar(r[i], m1, width,label=f'm1-{scheduler}',
           edgecolor=colors[i][0], fill = False, hatch=hatch[i][0]
           )
    
    # plt.bar(r[i], m12, width,bottom=m11,label=f'm1-2-{scheduler}',
    #        edgecolor=colors[i][0], fill = False, hatch=hatch[i][0])
    
    # plt.bar(r[i], m13, width,bottom=m11+m12,label=f'm1-3-{scheduler}',
    #        edgecolor=colors[i][0], fill = False, hatch=hatch[i][0])
    
    # plt.bar(r[i], m14, width,bottom=m11+m12+m13,label=f'm1-4-{scheduler}',
    #        edgecolor=colors[i][0], fill = False, hatch=hatch[i][0])
    
    
    plt.bar(r[i], m2, width,bottom=m1,label = f'm2-{scheduler}',
           edgecolor=colors[i][1], fill = False, hatch =hatch[i][1]
           )
    
    #ax.set_xticklabels(task_types)
    #ax.set_yticks(np.arange(0, 81, 10))
    
    i+=1
#ax.set_ylim(0,100)
plt.ylabel('Assignment%')
plt.title('Task Types')
plt.xticks([r0+(n-1)*0.5*width, r0+(n-1)*0.5*width + n*width+d ])
ax.set_xticklabels(task_types)
#plt.legend()
l5 = plt.legend(bbox_to_anchor=(1.0,1), loc="upper left", 
                 ncol=1)
plt.savefig('./results/figures/task_based_assignment_6-2_just_for_TT1.pdf', 
            bbox_inches='tight',dpi=300)
plt.show()