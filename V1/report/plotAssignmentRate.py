#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 10:14:25 2021

@author: c00424072
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

workload = 'compound-4'
scheduler = 'EE'
sample = '0'
time_interval = 5.0

path_to_result = f'./results/data/workload-{workload}/{scheduler}'
report = pd.read_csv(f'{path_to_result}/detailed-{sample}.csv',
                     usecols=['arrival_time','assigned_machine','status',
                              'missed_time'])
report = report.dropna(subset=['assigned_machine'],axis=0)



#report = report.loc[((report['status']=='MISSED') | (report['status']=='CANCELLED')),:]
#report = report.loc[report['assigned_machine'] !=np.nan ,:]

#report = report.drop(['extended_deadline'], axis = 1)
report = report.reset_index(drop=True)

max_interval = report['arrival_time'].max()  
interval_count = np.floor(max_interval / time_interval).astype('int')   
intervals = np.linspace(0, time_interval*interval_count,
                                interval_count+1)    
intervals[-1] = max_interval

#machine_types = report.loc[report.assigned_machine.notnull(),'assigned_machine'].unique()
machine_types = report.loc[:,'assigned_machine'].unique()
rate_columns = [f'MapRate-{machine_type}' for machine_type in machine_types]
#columns = np.concatenate((['start','end', 'MapRate-total','CancelRate'],rate_columns))
columns = np.concatenate((['start','end', 'MapRate-total'],rate_columns))
map_rate = pd.DataFrame(data={'start':intervals,
                                  'end': intervals}
                            , columns = columns)
map_rate['end'] = map_rate['end'].shift(-1, fill_value=0)
map_rate = map_rate.drop(index = map_rate.index[-1])

for idx, row in map_rate.iterrows():

    s =  row['start']
    e = row['end']
    
    
    for machine_type in machine_types:
        df = report[report['assigned_machine'] == machine_type]
        map_rate.loc[idx,f'MapRate-{machine_type}'] = df.loc[ ( (df.arrival_time < e) &
                                                      (df.arrival_time >= s)),
                                                    'arrival_time'].count()
    map_rate.loc[idx,'MapRate-total'] = report.loc[ ( (report.arrival_time < e) &
                                                      (report.arrival_time >= s)),
                                                    'arrival_time'].count()
    # map_rate.loc[idx,'CancelRate'] = report.loc[ ( (report.arrival_time < e) &
    #                                                   (report.arrival_time >= s)&
    #                                                   (report.status == 'CANCELLED')),
    #                                                 'arrival_time'].count()
map_rate = map_rate.rename(columns={'start':'time'})
map_rate = map_rate.drop('end',axis = 1)
map_rate.iloc[:,1:] = map_rate.iloc[:,1:].astype('int')


width = 16
height = 4
markers = ['o', 'x', '<', 's']
plt.figure(figsize=(width,height))
i=0
for column in map_rate.iloc[:,2:].columns:
    if column == 'MapRate-total':
        label = 'All'
    # elif column =='CancelRate':
    #     label = 'Cancelled'
    else:
        label = column.split('-')[1]
    plt.step(map_rate.time,
      map_rate[column].values,
      linestyle='--', marker=markers[i],alpha=0.9, label=label)
    i+=1
#plt.xticks(arrival_rate.time[0::5])
plt.ylabel(f'Assignment Rate')
plt.xlabel('Time')
plt.title(f'Assignment Rate  (#tasks per {time_interval} seconds)')
plt.grid()
plt.legend()
#plt.savefig(f'./results/figures/map_rate_{scheduler}_{workload}_{time_interval}sec.pdf',dpi=300)