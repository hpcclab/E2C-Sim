import pandas as pd
import numpy as np
import os
from scipy import stats
import shutil


def calculate_sep(etc):
    S_T = etc.max(axis=0) / etc
    S_M = etc.divide(etc.max(axis=1), axis=0)
    S_M = 1 / S_M

    S_T_AVG = np.mean(stats.hmean(S_T))
    S_M_AVG = stats.hmean(np.mean(S_M, axis=1))
    S_0 = S_T_AVG * S_M_AVG
    new_SEP = etc.max().max() / S_0

    return new_SEP




#path_to_etcs = '../../my_research/task_machine_performance/heterogeneous-arithmetic'
path_to_etcs = '../../from_server/task_machine_performance/heterogeneous-arithmetic'
#path_to_etcs = '../task_machine_performance/SEP_test_arrival'
#path_to_temp ='../../my_research/task_machine_performance/temp'
path_to_temp ='../../from_server/temp'
#path_to_temp = '/home/C00424072/Ali/Projects/E2C-Sim/V1/task_machine_performance/temp'
arrival_rate = 'arrival_1_0'

SEPs = os.listdir(path_to_etcs)

for SEP in SEPs:
    
    etc_files = os.listdir(f'{path_to_etcs}/{SEP}')
    if 'execution_times.csv' in etc_files:
        etc_files.remove('execution_times.csv')
    

    for etc_file in etc_files:        
        etc_id = etc_file.split('-')[1].split('.')[0]
        etc = pd.read_csv(f'{path_to_etcs}/{SEP}/{etc_file}', index_col=[0])
        new_SEP = calculate_sep(etc)


        print(f'Arithmetic SEP: {SEP} -->> {new_SEP}')
        # #dest = f'../../my_research/task_machine_performance/heterogeneous_mixed_arithmetic_harmonic/{new_SEP:3.0f}'
        # dest = f'../../from_server/task_machine_performance/heterogeneous_mixed_arithmetic_harmonic/{new_SEP:3.0f}'
        # #dest = f'../task_machine_performance/SEP_test_arrival/{new_SEP:3.0f}'
        # os.makedirs(f'{dest}/', exist_ok = True)
        # dest_etcs = os.listdir(dest)
        # shutil.copyfile(f'{path_to_etcs}/{SEP}/{etc_file}', f'{path_to_temp}/{etc_file}')
        # k=0
        # while etc_file in dest_etcs:
        #     etc_file = f'etc-{etc_id}-{k}.csv'
        #     k+=1        
        # os.rename(f'{path_to_temp}/etc-{etc_id}.csv', f'{path_to_temp}/{etc_file}')
        # shutil.copyfile(f'{path_to_temp}/{etc_file}', f'{dest}/{etc_file}')
       
       
        etc_folder = f'etc_{etc_id}'
        #dest = f'../../my_research/output/data/{arrival_rate}/heterogeneous_mixed_arithmetic_harmonic/{new_SEP:3.0f}'
        dest = f'../../from_server/data/{arrival_rate}/heterogeneous_mixed_arithmetic_harmonic/{new_SEP:3.0f}'
        os.makedirs(f'{dest}/', exist_ok = True)
        dest_etcs = os.listdir(dest)
        
        #shutil.copytree(f'../../my_research/output/data/{arrival_rate}/heterogeneous-arithmetic/{SEP}/{etc_folder}', f'../../my_research/output/data/temp/{etc_folder}')
        shutil.copytree(f'../../from_server/data/{arrival_rate}/heterogeneous-arithmetic/{SEP}/{etc_folder}', f'../../from_server/temp/{etc_folder}')
        k=0
        while etc_folder in dest_etcs:
            etc_folder = f'etc_{etc_id}_{k}'
            k+=1        
        # os.rename(f'../../my_research/output/data/temp/etc_{etc_id}', f'../../my_research/output/data/temp/{etc_folder}')
        # shutil.copytree(f'../../my_research/output/data/temp/{etc_folder}', f'{dest}/{etc_folder}')
        # shutil.rmtree(f'../../my_research/output/data/temp/{etc_folder}')

        os.rename(f'../../from_server/temp/etc_{etc_id}', f'../../from_server/temp/{etc_folder}')
        shutil.copytree(f'../../from_server/temp/{etc_folder}', f'{dest}/{etc_folder}')
        shutil.rmtree(f'../../from_server/temp/{etc_folder}')








        