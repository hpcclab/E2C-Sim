#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 19:03:37 2021

@author: Ali Mokhtari
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_arrivals(rate, task_hete,path_to_folder='./Episodes/Workloads'):
    #np.random.seed(10)
    #rnd = np.random.randint(0,29)
    rnd = 0
    path = f'{path_to_folder}/workload-{rate}-{task_hete}/ArrivalTimes-{rnd}.csv'
    arrivals = pd.read_csv(path, usecols = [' task_type_id',' arrival_time'])
    arrivals = arrivals.rename(columns={' arrival_time':'arrival_time',
                                        ' task_type_id':'task_type_id'})
    arrivals.loc[:,'inter_arrival'] = arrivals['arrival_time'] - \
                                arrivals['arrival_time'].shift(1,fill_value=0)
    return arrivals

def calculate_arrival_rate(arrivals, time_interval):
    
        
    max_arrival = arrivals['arrival_time'].max()        
    interval_count = np.floor(max_arrival / time_interval).astype('int')   
    arrival_intervals = np.linspace(0, time_interval*interval_count,
                                    interval_count+1)    
    arrival_intervals[-1] = max_arrival
    
    task_type_ids = arrivals.task_type_id.unique()
    rate_columns = [f'rate-{id}' for id in task_type_ids]
    columns = np.concatenate((['start','end', 'rate-total'],rate_columns))
    arrival_rate = pd.DataFrame(data={'start':arrival_intervals,
                                      'end': arrival_intervals}
                                , columns = columns)
    arrival_rate['end'] = arrival_rate['end'].shift(-1, fill_value=0)
    arrival_rate = arrival_rate.drop(index = arrival_rate.index[-1])
    
    for idx, row in arrival_rate.iterrows():
    
        s =  row['start']
        e = row['end']
        
        for task_type_id in task_type_ids:
            df = arrivals[arrivals['task_type_id'] == task_type_id]
            arrival_rate.loc[idx,f'rate-{task_type_id}'] = df.loc[ ( (df.arrival_time < e) &
                                                          (df.arrival_time >= s)),
                                                        'arrival_time'].count()
        arrival_rate.loc[idx,'rate-total'] = arrivals.loc[ ( (arrivals.arrival_time < e) &
                                                          (arrivals.arrival_time >= s)),
                                                        'arrival_time'].count()
    arrival_rate = arrival_rate.rename(columns={'start':'time'})
    arrival_rate = arrival_rate.drop('end',axis = 1)
    arrival_rate.iloc[:,1:] = arrival_rate.iloc[:,1:].astype('int')
    return arrival_rate

def plot_arrivals(arrival_rate, width=16, height=4):
    
    time_interval = arrival_rate.loc[1,'time'] - arrival_rate.loc[0,'time']
    plt.figure(figsize=(width,height))
    for column in arrival_rate.iloc[:,1:].columns:
        if column == 'rate-total':
            label = 'All'
        else:
            label = f'Task Type - {column.split("-")[1]}'
        plt.step(arrival_rate.time,
          arrival_rate[column].values,
          linestyle='--', alpha=0.8, label=label)
    #plt.xticks(arrival_rate.time[0::5])
    plt.ylabel(f'Arrival Rate')
    plt.xlabel('Time')
    plt.title(f'Arrival Rate  (#tasks arrival per {time_interval} seconds)')
    plt.grid()
    plt.legend()
    
    

arrivals = read_arrivals(5,3)
arrival_rate = calculate_arrival_rate(arrivals,5)
plot_arrivals(arrival_rate)




