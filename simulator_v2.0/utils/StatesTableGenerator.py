import numpy as np
import pandas as pd
import csv




no_task_types = 2
no_machine_types = 2

batch_qsize = 3
machine_qsize = 1

no_prog_levels = 4


task_types = [-1]
machine_types = [-1]
prog_levels = [-1]

for a_type in range(1, no_task_types+1):
    task_types.append(a_type)

for a_type in range(1, no_machine_types+1):
    machine_types.append(a_type)

for a_level in range(no_prog_levels):
    prog_levels.append(a_level)

columns = []

for machine in range(no_machine_types):
    columns.append('m{}_prog_level'.format(machine+1))
    columns.append('m{}_running_type'.format(machine+1))
    
    for q in range(machine_qsize):
        columns.append('m{}_q{}'.format(machine+1,q+1))

for bq in range(batch_qsize):
    columns.append('bq_{}'.format(bq+1))
    
    
df_state = pd.DataFrame(data = None, columns=columns)

for machine in range(1, no_machine_types +1):
    
    for pt in prog_levels:
        if pt != -1:
            df_state['m{}_prog_level'.format(machine)] = pt
            
            for tt in task_types:
                if tt != -1:
                    df_state['m{}_running_type'.format(machine)] = tt
                    

