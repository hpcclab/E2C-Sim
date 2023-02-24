
import pandas as pd
import csv
from os import makedirs, listdir

from utils.simulator import Simulator
from utils.machine import Machine
import utils.config as config

#rate = 'high'
#hete_homo = 'heterogeneous'

scenario = 'SEP_test_arrival_100000_0'
etc_folder = 'SEP_test_arrival'
SEPs = listdir(f'./task_machine_performance/{etc_folder}/')
#SEPs = ['1_0']
workloads = range(30)
#etcs = range(1)
etcs= ['heterogeneous_self_generated']
for SEP in SEPs:
    for etc_id in etcs:
        
        config.init()
        path_to_etc = f'./task_machine_performance/{etc_folder}/{SEP}/etc-{etc_id}.csv'
        #path_to_etc = f'./samples/{rate}/etc_{hete_homo}.csv'
        df = pd.read_csv(path_to_etc)
        df['idx'] = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']
        #df['idx'] = ['T1']
        df = df.set_index(['idx'])

        df.to_csv(path_to_etc)
        path_to_reports = f'./output/data/{scenario}/{etc_folder}/{SEP}/etc_{etc_id}'
        makedirs(f'{path_to_reports}/{config.scheduling_method}', exist_ok = True)
        report_summary = open(f'{path_to_reports}/{config.scheduling_method}/results-summary.csv','w')    
        report_header = ['workload_id', 'total_no_of_tasks','mapped','cancelled','URG_missed','BE_missed','Completion%','xCompletion%','totalCompletion%','wasted_energy%','consumed_energy%','energy_per_completion%']
        report = csv.writer(report_summary)  
        report.writerow(report_header)
        print(f'SEP:{SEP} ETC#: {etc_id} Scheduler: {config.scheduling_method}')
        for workload_id in workloads:
            
            config.init()     
            path_to_arrivals = f'./workloads/{scenario}/workload-{workload_id}.csv'
            #path_to_arrivals = f'./samples/{rate}/workload_{rate}.csv'
            m_id = 0
            for machine_type in config.machine_types:
                for r in range(1,machine_type.replicas+1):
                    specs = {'power': machine_type.power, 'idle_power':machine_type.idle_power}
                    machine = Machine(m_id,r, machine_type, specs)
                    config.machines.append(machine)            
                    m_id += 1
                
            simulation = Simulator(path_to_arrivals, path_to_etc, path_to_reports, seed = 123)
            simulation.set_scheduling_method(config.scheduling_method)        
            simulation.run()           
            row = simulation.report()
            report.writerows(row) 
                    

        config.log.close()        
        report_summary.close()            
        df_summary = pd.read_csv(f'{path_to_reports}/{config.scheduling_method}/results-summary.csv', 
        usecols=['totalCompletion%',
        'consumed_energy%','wasted_energy%'])
        print('\n\n'+ 10*'*'+f'  ||{scenario} || {etc_folder} --> {path_to_arrivals}: <<{config.scheduling_method}>> '+10*'*')
        #print(df_summary.mean())





