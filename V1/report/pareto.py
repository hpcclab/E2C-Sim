#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 20:59:49 2022

@author: c00424072
"""

import matplotlib.pyplot as plt

energy = [6928.2, 6876,  6750, 6640.2, 6719.4, 6453.0,6868.8 ]
missed = [29.7,   28.2,  19, 19.47, 21.05, 21.3,25.25]
heuristics = ['MM', 'ME', 'EE-defer-2-drop','EE-defer-1-drop',
              'EE-defer-3-drop',
              
              'EE-drop',
              'Random']

i=0
for i in range(len(heuristics)):
    
    plt.plot(energy[i],missed[i],'o', label = heuristics[i])

plt.xlabel('Energy Consumption [KJ]')
plt.ylabel('Missed Rate')
plt.grid()
plt.legend()
plt.show()