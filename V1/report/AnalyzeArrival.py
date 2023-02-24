import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


path = './Episodes/ArrivalTimes/'
arrival_times = []

with open(path+'ArrivalTimes-0.txt','r') as datafile:
    
    rows = datafile.readlines()
    for row in rows:
        if row[0] != '#':
            arrival_time = float(row.split(',')[2])
            arrival_times.append(arrival_time)

arrival_times = np.array(arrival_times)

df = pd.DataFrame(arrival_times, columns=['arrival_time'])
#df['time_diff'] = df['arrival_time'].shift(1)
df['time_dff'] = df['arrival_time'] - df['arrival_time'].shift(1)
df = df.dropna()

#df['time_dff'].plot.hist(bins=30)
df['arrival_time'].plot.hist(bins=30)

# =============================================================================
# task_type = '2'
# machine_type = 'g3sxlarge'
# path = '../data/execution_times/'
# execution_times = []
# 
# with open(path+task_type+'-'+machine_type+'.csv','r') as csvfile:
#     
#     rows = csv.reader(csvfile)
#     for row in rows:               
#         execution_time = float(row[0])
#         execution_times.append(execution_time)
# 
# execution_times = np.array(execution_times)
# print(np.mean(execution_times))
# 
# plt.hist(execution_times, bins=50, density=0 ,histtype = 'step')
# =============================================================================
