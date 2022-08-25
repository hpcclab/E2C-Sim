#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 17:27:02 2022

@author: Ali Mokhtari
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


errors = [11, 28, 15, 20]
cold_starts = [15, 22, 55, 58]
labels = ['iws-BFE', 'WS-BFE', 'BFE', 'LFE']
colors = ['red', 'blue', 'grey', 'yellow', 'olive']
#hatches = ['x','+', '//', '..']

points = list(zip(errors, cold_starts))


fig, ax = plt.subplots(1)
for idx , p in enumerate(points):
    
    ax.add_patch(Rectangle(p,100-p[0], 100-p[1], fill=True, color = colors[idx],
                           #hatch=hatches[idx],
                           alpha=0.7,
                           ec=colors[idx],
                           linewidth=2,
                           zorder=idx))
    ax.scatter(p[0], p[1], color=colors[idx], alpha =1.0 , label = labels[idx], ec='k', zorder=10)
    if labels[idx] == 'BFE':
        ax.text(p[0]-3, p[1]+3, labels[idx],
                bbox=dict(boxstyle="round",
                       ec='white',
                       fc='white',
                       ))
    elif labels[idx] == 'LFE':
        ax.text(p[0]+2, p[1]+3, labels[idx],
                bbox=dict(boxstyle="round",
                       ec='white',
                       fc='white',
                       ))
        
    else:
        ax.text(p[0]+2, p[1]+5, labels[idx],
                bbox=dict(boxstyle="round",
                       ec='white',
                       fc='white',
                       ))
    
   
#ax.legend(ncol=4)
ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.set_xlabel('model error (%)', fontsize = 14)
ax.set_ylabel('cold-start inference (%)', fontsize = 14)
ax.set_rasterized(True)
plt.tight_layout()
plt.savefig('./pareto_memory_management.pdf', dpi=300)
plt.show()



