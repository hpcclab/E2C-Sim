#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 14:40:12 2022

@author: c00424072
"""
import pandas as pd
import matplotlib.pyplot as plt

schedulers = ['EE', 'MM']

fig = plt.figure()
ax1 = fig.add_subplot(111)

markers = ['o', 'x', '<', 's','>','+']
#colors = ['navy','darkred','green','orange','']

df = pd.read_csv('./completion-vs-energy.csv')
rates = df.loc[:,'rate'].unique()


i=0
for rate in [7]:
    
    for scheduler in schedulers:
        
        y = df.loc[df['rate'] == rate,scheduler+'-completion'].astype(float)    
        #x = 3.6*(df.loc[df['rate'] == rate,scheduler+'-energy_consumption'].astype(float))
        x =df.loc[df['rate'] == rate,scheduler+'-energy_consumption'].astype(float)
        x = 100*(x/13)
        
        if scheduler == 'MM':
            ls = '-'
        else:
            ls = '--'
        
        ax1.plot(x.values, y.values, marker = markers[i],
                  #color = colors[i],
                  linestyle =ls,
                  label = f'{scheduler}')
        i += 1
    



plt.legend()
plt.xlabel('%Available Energy')
plt.ylabel('%Completion')
plt.xticks(range(0,110,10))
plt.grid()

plt.savefig('./results/figures/completion_vs_energy_compound-4.pdf',dpi=300)
plt.show()