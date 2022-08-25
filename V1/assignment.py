#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 02:26:00 2022

@author: c00424072
"""
import matplotlib.pyplot as plt


"""
"scheduling_policy = ['FCFS', 'MEET', 'MECT', 'MM', 'MSD', 'MMU']\n",
    "low = [56, 100, 100, 100, 100, 100]\n",
    "medium = [47, 58, 99, 82, 78, 88]\n",
    "high = [33, 19, 29, 34, 30, 37]\n"
"""


colors =['navy', 'darkred', 'orange', 'darkgreen', 'grey', 'purple']

schedulers = ['FCFS', 'MEET', 'MECT', 'MM', 'MSD', 'MMU']
completions = [[56, 100, 100, 100, 100, 100],
               [47, 58, 99, 82, 78, 88],
               [33, 19, 29, 34, 30, 37]]

w = 1.0
d = 1.5


r0 = [0, len(schedulers)*w+d, 2*(len(schedulers)*w+d)]
plt.figure(figsize=(10,4))

for i, completion in enumerate(completions):
    
    
    r = [r0[i]+k*w for k in range(len(schedulers))]
    
    for j, scheduler in enumerate(schedulers):
        if i==1:
            plt.bar(r[j], completion[j], width=w, color=colors[j], alpha=0.7, label=scheduler)
        else:
            plt.bar(r[j], completion[j], width=w, color=colors[j], alpha=0.7)

plt.legend(ncol=2)
print(r0)
r = [r0[m]+0.5*len(schedulers)*w-0.5*w for m in range(len(completions))]
print(r)
plt.xticks(r, ['low', 'medium', 'high'])
plt.xlabel('arrival rate')
plt.ylabel('%completion')
plt.title('Heterogeneous')
plt.savefig('heterogeneous_assignment.jpg', dpi=300, bbox_inches='tight')