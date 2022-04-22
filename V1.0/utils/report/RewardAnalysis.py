#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 09:49:02 2021

@author: c00424072
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




no_of_iter = 86
path = './results/validation'

detailed_reward = ['completion_gain', 'energy_loss', 'defer', 'drop',
       'wrong_task_selection', 'full_machine_mapping', 'reward']

detailed_reward = ['completion_gain', 'energy_loss', 'defer', 'drop',
       'wrong_task_selection', 'full_machine_mapping', 'reward']

xcompletion = []
completion = []
energy = []
total_completion = []

average_reward = pd.DataFrame(columns=['completion_gain', 'energy_loss', 'defer', 'drop',
       'wrong_task_selection', 'full_machine_mapping', 'reward'])
max_reward = []

for i in range(no_of_iter):
    total_reward = pd.DataFrame(columns=['completion_gain', 'energy_loss', 'defer', 'drop',
       'wrong_task_selection', 'full_machine_mapping', 'reward'])  
    
    
    for k in range(15):    
        rewards = pd.read_csv(f'{path}/{i}/rewards-{k}.csv')        
        rewards = rewards.drop('Unnamed: 0',axis=1)
        rewards['energy_loss'] = -1 * rewards['energy_loss']
        total_reward = total_reward.append(rewards.sum(axis=0).round(1), ignore_index=True)        
   
      
    average_reward = average_reward.append(total_reward.mean(axis=0), ignore_index = True)        
    max_reward.append(total_reward.max(axis=0))
    
    results = pd.read_csv(f'{path}/{i}/results-summary.csv')
    xcompletion.append(results['xCompletion%'].round(2).mean(axis=0))
    completion.append(results['Completion%'].round(2).mean(axis=0))
    total_completion.append(results['totalCompletion%'].round(2).mean(axis=0))
    energy.append(results['consumed_energy%'].round(2).mean(axis=0))


plt.figure(figsize=(16,8))
markers = ['o','','3','4','|', '_','+']
linestyles = ['-','--',':','-',(0, (1, 10)),(0, (5, 10)),(0, (3, 10, 1, 10, 1, 10)) ]
i = 0
for clm in detailed_reward:
    plt.plot(average_reward[clm], marker = markers[i], linestyle= linestyles[i],
             label = clm)
    i+=1

plt.title('The RL Model Evaluation on the Validation Workload')
plt.ylabel('Total Reward')
plt.xlabel('Iterations')
plt.grid()
plt.legend()    
plt.savefig('./figures/reward_analysis.jpg')
#iterations = list(range(no_of_iter))
#plt.plot(iterations, total_completion,'-o')
