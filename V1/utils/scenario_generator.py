import pandas as pd
import numpy as np


arrival_rates = np.concatenate(([0.001],np.linspace(0.01,0.19,19) , np.linspace(0.2,1.0,9),np.linspace(2,5,4), [10, 100000]) )
#arrival_rates = [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19]
arrival_rates = np.round(arrival_rates,3)
for arrival_rate in arrival_rates:
    
    no_of_task_type = 1
    no_of_tasks = [500 for i in range(no_of_task_type)]
    end_time = sum(no_of_tasks)/arrival_rate
    #arrival_rate = str(round(sum(no_of_tasks)/ end_time, 2))
    arrival_rate = str(round(arrival_rate,3)).replace('.', '_')


    scenario = pd.DataFrame(columns = ['task_type_id', 'start_time', 'end_time', 'distribution', 'number'])

    for task_type_id in range(1,no_of_task_type+1):
        scenario.loc[task_type_id-1]=[f'T{task_type_id}', 0, end_time, 'exponential', no_of_tasks[task_type_id-1]]

    scenario.to_csv(f'./workloads/scenarios/SEP_test_arrival_one_type_{arrival_rate}.csv', index=False)




