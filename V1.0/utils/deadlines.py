import pandas as pd


het_id = 'het-42'
path = f'../workload/execution_times/{het_id}'
no_of_tasks = 4
no_of_machines = 4
slack_factor = 1.05

et_all = pd.DataFrame(data=None, columns =['execution_time'])
avg_tt = pd.DataFrame(columns=[f'T{i}' for i in range(1, 1 + no_of_tasks)], index= [0])
deadlines = pd.DataFrame(columns=[f'T{i}' for i in range(1, 1 + no_of_tasks)], index= [0])

for tt in range(1, 1 + no_of_tasks):
    et_tt = pd.DataFrame(data=None, columns =['execution_time'])    
    
    for m in range(1, 1+no_of_machines):
        data = pd.read_csv(f'{path}/{tt}-m{m}.csv')
        et_tt = et_tt.append(data, ignore_index=True)
        et_all = et_all.append(data, ignore_index=True)
        
    avg_tt.loc[0,f'T{tt}'] = et_tt['execution_time'].mean()
    
avg_all = et_all['execution_time'].mean()

for tt in range(1, 1 + no_of_tasks):
   
    delta = avg_tt.loc[0,f'T{tt}'] + slack_factor * avg_all
    delta = round(delta, 1)
    deadlines.loc[0,f'T{tt}'] = delta
#deadlines.to_csv(f'../workload/execution_times/deadlines-{het_id}.csv',index = False)
print(deadlines)