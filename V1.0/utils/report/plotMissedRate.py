#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 21:43:42 2021

@author: c00424072
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

workload = '1-3'
scheduler = 'MM'
sample = '0'
time_interval = 15.0

path_to_result = f'../../output/data/{workload}/{scheduler}'
report = pd.read_csv(f'{path_to_result}/detailed-{sample}.csv',
                     usecols=['arrival_time','assigned_machine','status',
                              'extended_deadline','missed_time'])

max_deadline = report['extended_deadline'].max()

report = report.loc[((report['status']=='MISSED') | (report['status']=='CANCELLED')),:]

report = report.drop(['extended_deadline'], axis = 1)
report = report.reset_index(drop=True)

    
interval_count = np.floor(max_deadline / time_interval).astype('int')   
intervals = np.linspace(0, time_interval*interval_count,
                                interval_count+1)    
intervals[-1] = max_deadline

machine_types = report.loc[report.assigned_machine.notnull(),'assigned_machine'].unique()
rate_columns = [f'MissRate-{machine_type}' for machine_type in machine_types]
columns = np.concatenate((['start','end', 'MissRate-total','CancelRate'],rate_columns))
missed_rate = pd.DataFrame(data={'start':intervals,
                                  'end': intervals}
                            , columns = columns)
missed_rate['end'] = missed_rate['end'].shift(-1, fill_value=0)
missed_rate = missed_rate.drop(index = missed_rate.index[-1])

for idx, row in missed_rate.iterrows():

    s =  row['start']
    e = row['end']
    
    
    for machine_type in machine_types:
        df = report[report['assigned_machine'] == machine_type]
        missed_rate.loc[idx,f'MissRate-{machine_type}'] = df.loc[ ( (df.missed_time < e) &
                                                      (df.missed_time >= s)),
                                                    'missed_time'].count()
    missed_rate.loc[idx,'MissRate-total'] = report.loc[ ( (report.missed_time < e) &
                                                      (report.missed_time >= s)),
                                                    'missed_time'].count()
    missed_rate.loc[idx,'CancelRate'] = report.loc[ ( (report.arrival_time < e) &
                                                      (report.arrival_time >= s)&
                                                      (report.status == 'CANCELLED')),
                                                    'arrival_time'].count()
missed_rate.loc[:,'MissRate-total'] = missed_rate['MissRate-total'] + missed_rate['CancelRate']
missed_rate = missed_rate.rename(columns={'start':'time'})
missed_rate = missed_rate.drop('end',axis = 1)
missed_rate.iloc[:,1:] = missed_rate.iloc[:,1:].astype('int')


width = 16
height = 4
markers = ['o', 'x', '<', 's']
ls = ['-',':','--']
plt.figure(figsize=(width,height))
i=0
for column in missed_rate.iloc[:,2:].columns:
    if column == 'MissRate-total':
        label = 'All'
    elif column =='CancelRate':
        label = 'cancelled'
    else:
        label = f"{column.split('-')[1]}"
    plt.step(missed_rate.time,
      missed_rate[column].values,
      linestyle=ls[i],
      marker=markers[i],  
      linewidth = 3,
      alpha=0.9, label=label)
    i+=1
    


plt.ylabel(f'unsuccessful completion rate', fontsize = 17)
plt.xlabel('time', fontsize = 18)
plt.xticks(fontsize =15)
plt.yticks(fontsize =15)
#plt.ylim([0,30])
#plt.title(f'Miss Rate  (#tasks per {time_interval} seconds)')
plt.grid(linestyle='dotted')
plt.legend(fontsize = 16, ncol=3)
# plt.savefig(f'../../output/figures/miss_rate_{scheduler}_{workload}_{time_interval}sec.pdf',
#             bbox_inches='tight',pad_inches = 0,dpi=300)