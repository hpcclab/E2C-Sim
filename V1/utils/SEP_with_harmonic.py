import pandas as pd
import numpy as np
import os
from scipy.stats import hmean
import shutil




def calculate_sep(etc):
    S_T = etc.max(axis=0) / etc
    S_M = etc.divide(etc.max(axis=1), axis=0)
    S_M = 1 / S_M

    S_T_AVG = hmean(hmean(S_T))
    S_M_AVG = hmean(hmean(S_M))
    S_0 = S_T_AVG * S_M_AVG
    new_SEP = etc.max().max() / S_0

    return new_SEP




path_to_etcs = '../../my_research/task_machine_performance/heterogeneous-arithmetic'
arrival_rate = 'arrival_10_0'

SEPs = os.listdir(path_to_etcs)

for SEP in SEPs:
    etc_files = os.listdir(f'{path_to_etcs}/{SEP}')
    if 'execution_times.csv' in etc_files:
        etc_files.remove('execution_times.csv')
    
    for etc_file in etc_files:        
        etc_id = etc_file.split('-')[1].split('.')[0]
        etc = pd.read_csv(f'{path_to_etcs}/{SEP}/{etc_file}', index_col=[0])
        new_SEP = calculate_sep(etc)
        dest = f'../../my_research/task_machine_performance/heterogeneous_arithmetic_to_harmonic/{new_SEP:3.0f}'
        os.makedirs(f'{dest}/', exist_ok = True)
        dest_etcs = os.listdir(dest)
        shutil.copyfile(f'{path_to_etcs}/{SEP}/{etc_file}', f'../../my_research/task_machine_performance/temp/{etc_file}')
        k=0
        while etc_file in dest_etcs:
            etc_file = f'etc-{etc_id}-{k}.csv'
            k+=1        
        os.rename(f'../../my_research/task_machine_performance/temp/etc-{etc_id}.csv', f'../../my_research/task_machine_performance/temp/{etc_file}')
        shutil.copyfile(f'../../my_research/task_machine_performance/temp/{etc_file}', f'{dest}/{etc_file}')
        # etc_folder = f'etc_{etc_id}'
        # dest = f'../../my_research/output/data/{arrival_rate}/heterogeneous_arithmetic_to_harmonic/{new_SEP:3.0f}'
        # os.makedirs(f'{dest}/', exist_ok = True)
        # dest_etcs = os.listdir(dest)
        
        # shutil.copytree(f'../../my_research/output/data/{arrival_rate}/heterogeneous-arithmetic/{SEP}/{etc_folder}', f'../../my_research/output/data/temp/{etc_folder}')
        # k=0
        # while etc_folder in dest_etcs:
        #     etc_folder = f'etc_{etc_id}_{k}'
        #     k+=1        
        # os.rename(f'../../my_research/output/data/temp/etc_{etc_id}', f'../../my_research/output/data/temp/{etc_folder}')
        # shutil.copytree(f'../../my_research/output/data/temp/{etc_folder}', f'{dest}/{etc_folder}')
        # shutil.rmtree(f'../../my_research/output/data/temp/{etc_folder}')








        