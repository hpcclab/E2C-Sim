#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:37:11 2021

@author: c00424072
"""

import pandas as pd
import matplotlib.pyplot as plt


schedulers = ['EE','RLS','MM']
markers = ['o', 'x', '<', 's']
colors = ['blue', 'red', 'green', 'orange']
fig = plt.figure(figsize=(18,16))


df = pd.read_csv('./summary_of_results-50.csv')
df = df.drop(0, axis= 0 )
df = df.drop(['Unnamed: 0'], axis = 1)
df = df.reset_index(drop=True)
df = df.rename(columns = {'Unnamed: 2':'MM-Energy', 
                'Unnamed: 4':'ME-Energy',
                'Unnamed: 6':'EE-Energy',
                'Unnamed: 8':'TabRLS-Energy',
                'Unnamed: 10':'RLS-Energy'
                })

ax1 = fig.add_subplot(321)

i=0
for scheduler in schedulers:    
    y = df[scheduler].astype(float)
    
    ax1.plot(df.index.values, y.values, marker = markers[i],
            # color = colors[i],
             linestyle ='--',
             label = scheduler+'-50')
    i += 1
    
    

ax2 = fig.add_subplot(322)

i=0
for scheduler in schedulers:
    
    y = df[scheduler+'-Energy'].astype(float)
    
    ax2.plot(df.index.values, y.values, marker = markers[i],linestyle ='-',
            # color = colors[i],
             label = scheduler+'-50')
    i += 1
    
    
df = pd.read_csv('./summary_of_results-30.csv')
df = df.drop(0, axis= 0 )
df = df.drop(['Unnamed: 0'], axis = 1)
df = df.reset_index(drop=True)
df = df.rename(columns = {'Unnamed: 2':'MM-Energy', 
                'Unnamed: 4':'ME-Energy',
                'Unnamed: 6':'EE-Energy',
                'Unnamed: 8':'TabRLS-Energy',
                'Unnamed: 10':'RLS-Energy',
                })


ax3 = fig.add_subplot(323)

i=0
for scheduler in schedulers:
    
    y = df[scheduler].astype(float)
    
    ax3.plot(df.index.values, y.values, marker = markers[i],linestyle ='-',
            # color = colors[i],
             label = scheduler+'-30')
    i += 1
    
    

ax4 =fig.add_subplot(324)
i=0
for scheduler in schedulers:
    
    y = df[scheduler+'-Energy'].astype(float)
    
    ax4.plot(df.index.values, y.values, marker = markers[i],linestyle ='-',
            # color = colors[i],
             label = scheduler+'-30')
    i += 1
 



   
    
    
df = pd.read_csv('./summary_of_results-15.csv')
df = df.drop(0, axis= 0 )
df = df.drop(['Unnamed: 0'], axis = 1)
df = df.reset_index(drop=True)
df = df.rename(columns = {'Unnamed: 2':'MM-Energy', 
                'Unnamed: 4':'ME-Energy',
                'Unnamed: 6':'EE-Energy',
                'Unnamed: 8':'TabRLS-Energy',
                'Unnamed: 10':'RLS-Energy'
                })


ax5 = fig.add_subplot(325)

i=0
for scheduler in schedulers:
    
    y = df[scheduler].astype(float)
    
    ax5.plot(df.index.values, y.values, marker = markers[i],linestyle ='-',
            # color = colors[i],
             label = scheduler+'-15')
    i += 1
    
    

ax6 =fig.add_subplot(326)
i=0
for scheduler in schedulers:
    
    y = df[scheduler+'-Energy'].astype(float)
    
    ax6.plot(df.index.values, y.values, marker = markers[i],linestyle ='-',
            # color = colors[i],
             label = scheduler+'-15')
    i += 1
    
 
    
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax5.legend()
ax6.legend()
ax3.set_xlabel('Arrival Rate Intensity Index')
ax4.set_xlabel('Arrival Rate Intensity Index')


ax2.set_ylabel('Energy Consumption%')
ax4.set_ylabel('Energy Consumption%')
ax6.set_ylabel('Energy Consumption%')
ax1.set_ylabel('Completion%')
ax3.set_ylabel('Completion%')
ax5.set_ylabel('Completion%')


fig.savefig('./figures/compare_results-with-RLS.jpg', dpi=300)



######################################################################

fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(111)
df = pd.read_csv('./summary_of_results-50.csv')
df = df.drop(0, axis= 0 )
df = df.drop(['Unnamed: 0'], axis = 1)
df = df.reset_index(drop=True)
df = df.rename(columns = {'Unnamed: 2':'MM-Energy', 
                'Unnamed: 4':'ME-Energy',
                'Unnamed: 6':'EE-Energy',
                'Unnamed: 8':'TabRLS-Energy',
                'Unnamed: 10':'RLS-Energy'})
df = df.dropna()




schedulers = ['EE', 'MM', 'RLS']
markers = ['o', 'x', '<', 's']
colors = ['blue', 'red', 'green', 'orange']
i=0
for scheduler in schedulers:
    
    y = df[scheduler].astype(float)
    x = df[scheduler+'-Energy'].astype(float)
    
    ax1.plot(x.values, y.values, marker = markers[i],
             color = colors[i],
             linestyle ='--',
             label = scheduler+'-50')
    i += 1
   
    

    
    
df = pd.read_csv('./summary_of_results-30.csv')
df = df.drop(0, axis= 0 )
df = df.drop(['Unnamed: 0'], axis = 1)
df = df.reset_index(drop=True)
df = df.rename(columns = {'Unnamed: 2':'MM-Energy', 
                'Unnamed: 4':'ME-Energy',
                'Unnamed: 6':'EE-Energy',
                'Unnamed: 8':'TabRLS-Energy',
                'Unnamed: 10':'RLS-Energy',
                })



i=0
for scheduler in schedulers:
    
    y = df[scheduler].astype(float)
    x = df[scheduler+'-Energy'].astype(float)
    
    ax1.plot(x.values, y.values, marker = markers[i],linestyle ='-',
             color = colors[i],
             label = scheduler+'-30')
    i += 1
    

    
df = pd.read_csv('./summary_of_results-15.csv')
df = df.drop(0, axis= 0 )
df = df.drop(['Unnamed: 0'], axis = 1)
df = df.reset_index(drop=True)
df = df.rename(columns = {'Unnamed: 2':'MM-Energy', 
                'Unnamed: 4':'ME-Energy',
                'Unnamed: 6':'EE-Energy',
                'Unnamed: 8':'TabRLS-Energy',
                'Unnamed: 10':'RLS-Energy'
                })




i=0
for scheduler in schedulers:
    
    y = df[scheduler].astype(float)
    x = df[scheduler+'-Energy'].astype(float)
    
    ax1.plot(x.values, y.values, marker = markers[i],linestyle =':',
             color = colors[i],
             label = scheduler+'-15')
    i += 1
    

    
ax1.legend()
ax2.legend()
ax3.legend()


# ax1.arrow(85,40,-60,0, width=2, fc = 'white', ec='black')
# ax1.text(30,45,'More Intense Arrival Rate', fontsize =16,
#          fontweight='bold'
#          #bbox=dict(facecolor='white', alpha=1.0)
#          )

ax1.set_xlabel('Energy Consumption%')



ax1.set_ylabel('Completion%')
ax2.set_ylabel('Completion%')
ax3.set_ylabel('Completion%')
ax1.grid()
ax1.set_xticks(range(0,110,10))
ax1.set_yticks(range(0,110,10))

fig.savefig('./figures/compl_energy_compare_results-with-RLS.jpg', dpi=300)
