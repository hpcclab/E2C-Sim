
import pandas as pd
import numpy as np
import csv
from os import makedirs

from utils.simulator import Simulator
from utils.machine import Machine
import utils.config as config
from workload.generator import workloads_generator

from workload.workload import Workload

workload_name = 'heterogeneous'
scenarios = ['sc-2']
etcs = [f'etc-{i}' for i in range(100)]
workload_id_range = list(range(30))
workloads_exist = True
is_etc_exist = True
is_et_exist = True

def simulate(workload_name, scenarios, etcs, workload_id_range, workloads_exist=False,is_etc_exist = False, is_et_exist = False):
    for sc in scenarios:
        if not workloads_exist:    
            config.init()
            workloads_generator(workload_name,sc , is_etc_exist, is_et_exist ,
                        no_of_etcs = 1, et_set = [1,1,5,5,10,10,10,25,25,25,25,100,100,100,100,100, 150,150]  ,
                        et_variance=0.05, et_size=1000, sample_size = 30)
        for etc in etcs:
            config.init()            
            path_to_result = f'./output/data/{workload_name}/{sc}/{etc}/{config.scheduling_method}'        
            makedirs(path_to_result, exist_ok = True)
            report_summary = open(f'{path_to_result}/results-summary.csv','w')
            report_header = ['workload_id', 'total_no_of_tasks','mapped','cancelled','URG_missed','BE_missed','Completion%','xCompletion%','totalCompletion%','wasted_energy%','consumed_energy%','energy_per_completion%']
            report = csv.writer(report_summary)
            report.writerow(report_header) 
        
            for workload_id in workload_id_range:        
                config.init()
                id = 0
                for machine_type in config.machine_types:
                    for r in range(1,machine_type.replicas+1):
                        specs = {'power': machine_type.power, 'idle_power':machine_type.idle_power}
                        machine = Machine(id,r, machine_type, specs)
                        config.machines.append(machine)            
                        id += 1
                    
                simulation = Simulator(workload_name, sc, etc, workload_id) 
                simulation.create_event_queue()
                scheduler = config.get_scheduler()
                simulation.set_scheduling_method(scheduler)        
                simulation.run()   
                       
                row = simulation.report()   
                report.writerows(row)        
            report_summary.close()
            config.log.close()         
            df_summary = pd.read_csv(f'{path_to_result}/results-summary.csv', 
            usecols=['totalCompletion%',
            'consumed_energy%','wasted_energy%'])
            print('\n\n'+ 10*'*'+f'  <<{workload_name}>>||{sc} || {etc} --> {workload_id}: <<{config.scheduling_method}>> '+10*'*')
            print(df_summary.mean())



# config.init()
# workloads_generator(workload_name,scenarios[0] , is_etc_exist, is_et_exist ,
#             no_of_etcs = 1, et_set = [1,1,5,5,10,10,10,25,25,25,25,100,100,100,100,100, 150,150]  ,
#             et_variance=0.05, et_size=1000, sample_size = 30)


simulate(workload_name, scenarios, etcs, workload_id_range, workloads_exist,
          is_etc_exist,is_et_exist)


