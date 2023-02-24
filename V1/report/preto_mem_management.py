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


def is_pareto_frontier(costs):   
    is_frontier = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        is_frontier[i] = np.all(np.any(costs[:i]>c, axis=1)) and np.all(np.any(costs[i+1:]>c, axis=1))
    return is_frontier


df = pd.read_csv('./mem_pareto_delta.csv')
df['error(%)'] = 100 - df['accuracy(%)']
df = df.drop('accuracy(%)', axis=1)

# for idx, row in df.iterrows():
#     label = row['label']
#     label_split = label.split('-')
#     df.loc[idx, 'label'] = label_split[0] if len(label_split) ==2 else (label_split[0] +'-'+label_split[1])

labels = df['label'].unique()
colors = ['green', 'gray', 'blue', 'red', 'olive']

frontiers = []
for label in labels:
    policy_results = df[df['label']==label]
    points = policy_results.loc[:, ['cold-start inferences(%)', 'error(%)']].values
    df.loc[df['label']==label, 'frontiers'] = is_pareto_frontier(points)


colors = {'LFE': colors[0],
            'BFE': colors[1],
            'WS-BFE':colors[2],
            'iWS-BFE':colors[3]
        }
cmaps = {'LFE': 'Greys',
            'BFE': 'Reds',
            'WS-BFE':'Greens',
            'iWS-BFE':'Blues'
        }

markers = {'LFE': '<',
            'BFE': 'o',
            'WS-BFE':'P',
            'iWS-BFE': 's',
        }


fig, ax = plt.subplots(1)
order = {'LFE':2,
         'BFE':3,
         'WS-BFE':1,
         'iWS-BFE':0}

count_LFE =0
count_BFE=0
count_WS = 0

if label == 'BFE':
    alpha = 0.6
elif label == 'LFE':
    alpha= 0.9
elif label=='WS-BFE':
    alpha = 0.8
else:
    alpha =0.7
size =70  
    
for idx , row in df.iterrows():  
    
    label = row['label']
    frontier = row['frontiers']        
      
    if frontier :
        if row['cold-start inferences(%)'] <= 60:
            p = (row['error(%)'], row['cold-start inferences(%)'])
            
            if label=='BFE':
                ax.add_patch(Rectangle(p,100-p[0], 100-p[1], fill=True, 
                                    color = colors[label],
                                    #hatch=hatches[idx],
                                    alpha=alpha,
                                    ec=colors[label],
                                    linewidth=2,
                                    zorder=order[label]))
                
            else:
                ax.add_patch(Rectangle(p,100-p[0], 100-p[1], fill=True, 
                                        color = colors[label],
                                        #hatch=hatches[idx],
                                        alpha=alpha,
                                        ec=colors[label],
                                        linewidth=2,
                                        zorder=order[label]))
            
            if label == 'BFE' and count_BFE == 0 :
                ax.text(p[0]-7.5, p[1]-2, label,
                        color= colors[label],
                        bbox=dict(boxstyle="round",
                                  #ec=colors[label],
                                  fc='white',
                                  ))
                count_BFE +=1 
                
            elif label == 'LFE' and count_LFE ==0 :
                
                ax.text(p[0]-8, p[1]+3, label,
                        color = colors[label],
                        bbox=dict(boxstyle="round",
                                  #ec=colors[label],
                                  fc='white',
                                  ))
                count_LFE +=1
                
            elif label =='WS-BFE' and count_WS==0:
                ax.text(p[0]-5, p[1]-7, label,
                        color = colors[label],
                        bbox=dict(boxstyle="round",
                                  #ec=colors[label],
                                  fc='white',
                                  ))
                count_WS +=1
            elif label =='iWS-BFE':
                ax.text(p[0]-15, p[1]-3, label,
                        color = colors[label],
                        bbox=dict(boxstyle="round",
                                  #ec='white',
                                  fc='white',
                                  ))
                
            
        
    
    ax.scatter(row['error(%)'], row['cold-start inferences(%)'], 
                color='white',
                marker = markers[label],                 
                s = size,
                alpha =1.0 , label = label, ec='k', zorder=10)
    
#ax.legend(ncol=4)
ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.set_xlabel('model error (%)', fontsize = 14)
ax.set_ylabel('cold-start inference (%)', fontsize = 14)
ax.set_rasterized(True)
plt.tight_layout()
plt.savefig('./pareto_memory_management_more.jpg', dpi=300,bbox_inches='tight')
plt.show()


plt.figure()


for policy in ['LFE', 'BFE', 'WS-BFE', 'iWS-BFE']:
    
    df_policy =  df[df['label']==policy]
    df_policy = df_policy.sort_values('delta')
    #df_policy = df_policy[df_policy['delta']<55]
    x =df_policy['error(%)'].values
    y = df_policy['cold-start inferences(%)'].values
    c = df_policy['delta'].values
    # plt.scatter(x, y, 
    #            c= c,
    #            cmap=cmaps[policy],
    #            marker = markers[policy],
    #            s = size,               
    #            alpha =1.0 , label = policy, ec='k', zorder=10)
    plt.plot(c,y, label=policy, marker=markers[policy], color= colors[policy],
             markersize = 8)

# for idx , row in df.iterrows():      
#     label = row['label']
#     delta = row['delta']
#     p = (row['error(%)'], row['cold-start inferences(%)'])
#     plt.text(p[0]+0.5, p[1], delta,
#                         color = 'k')
    


plt.ylim([10,90])
plt.legend(loc=[0.1,0.9],ncol=4)
plt.ylabel('cold-start inferences (%)', fontsize = 14)
plt.xlabel(r'$\Delta$', fontsize=14)
plt.tight_layout()
plt.savefig('./cold_start_vs_delta.pdf', dpi=300,bbox_inches='tight')
plt.show()


plt.figure()


for policy in ['LFE', 'BFE', 'WS-BFE', 'iWS-BFE']:
    
    df_policy =  df[df['label']==policy]
    df_policy = df_policy.sort_values('delta')
    x =df_policy['error(%)'].values
    y = df_policy['cold-start inferences(%)'].values
    c = df_policy['delta'].values   
    plt.plot(c,x, label=policy, marker=markers[policy], color= colors[policy],
             markersize = 8)

    

plt.ylim([10,40])
plt.legend(loc=[0.1,0.8],ncol=4)
plt.ylabel('model error (%)', fontsize = 14)
plt.xlabel(r'$\Delta$', fontsize=14)
plt.tight_layout()
plt.savefig('./error_vs_delta.pdf', dpi=300, bbox_inches='tight')
plt.show()







