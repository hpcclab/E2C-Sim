#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 01:06:27 2022

@author: c00424072
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = '/home/C00424072/Desktop'
df = pd.read_csv(f'{path}/etc-4.csv', index_col=0)
df = df.round(2)

S_T = df.max(axis=0) / df
S_M = df.divide(df.max(axis=1), axis=0)
S_M = 1 / S_M
t_color = ['blue', 'red', 'orange', 'green']
m_marker = ['P', 'o', '<', 's']

for i in range(df.shape[0]):
    
    for j in range(df.shape[1]):
        
        x = S_M.iloc[i,j]
        y = S_T.iloc[i,j]
        
        if i==0:
            plt.scatter(x,y, color='none', edgecolor='k', marker=m_marker[j], label = f'M{j+1}') 
            plt.scatter(x,y, color=t_color[i], marker=m_marker[j]) 
        else:
            plt.scatter(x,y, color=t_color[i], marker=m_marker[j])
        



for j in range(df.shape[1]):
    
    bbox = dict(fc =t_color[j], color=t_color[j], pad=0.5)
    plt.annotate(rf'  $T_{j+1}$   ',
                xy=(1,5), xytext =(2.0,7.5-0.5*j),
                bbox = bbox,  rotation = 0,
                ha='center', va='bottom',
                verticalalignment='center',
                fontsize=14,
                fontweight='bold',
                color='white') 
    
            
        
            
       
        
plt.xlabel(r'speedup due to machine heterogeneity, $S^M$', fontsize=12)
plt.ylabel(r'speedup due to task heterogeneity, $S^T$', fontsize =12)
#plt.ylim(0,7)
plt.xlim(0,25)
plt.legend()
plt.tight_layout()
#plt.savefig(f'{path}/het_schematic_view.pdf', dpi=300)
plt.show()