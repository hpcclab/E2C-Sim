
import pandas as pd
import numpy as np
import csv
from os import makedirs

from utils.simulator import Simulator
from utils.machine import Machine
import utils.config as config
from gui import window
config.init()

if config.gui == 1:
    window()
else:
    scheduling_method = config.scheduling_method
    workload = '9-0'
    # het_level = 2
    # consistency_degree = 0
    low = 0
    high = 30

    no_of_iterations = 1
    train = 0

    # path_to_result = f'{config.settings["path_to_output"]}/data/H-{het_level}-a-{consistency_degree}/{workload}/{scheduling_method}'
    path_to_result = f'{config.settings["path_to_output"]}/data/{workload}/{scheduling_method}'
    makedirs(path_to_result, exist_ok = True)
    report_summary = open(f'{path_to_result}/results-summary.csv','w')
    summary_header = ['Episode', 'total_no_of_tasks','mapped','cancelled','URG_missed','BE_missed','Completion%','xCompletion%','totalCompletion%','wasted_energy%','consumed_energy%','energy_per_completion%']
    writer = csv.writer(report_summary)
    writer.writerow(summary_header)

    df_task_based_report = pd.DataFrame()

    count = 0 

    for i in range(low,high):
        
        # s = f'\n\nSample: {i}'
        # config.log.write(s)
        # print(s)  
        count += 1      
        Tasks = []        
        config.init()
            
        id = 0
        for machine_type in config.machine_types:
            for r in range(1,machine_type.replicas+1):
                specs = {'power': machine_type.power, 'idle_power':machine_type.idle_power}
                machine = Machine(id,r, machine_type, specs)
                config.machines.append(machine)

                id += 1
    
        #simulation = Simulator( het_level = het_level, consistency_degree= consistency_degree,workload_id = workload, epsiode_no = i , id=i) 
        simulation = Simulator( workload_id = workload, epsiode_no = i , id=i) 
        
        simulation.create_event_queue()
        simulation.set_scheduling_method()
        
        simulation.run()   
        #row, task_report = simulation.report(path_to_result)   
        row = simulation.report(path_to_result)   
        writer.writerows(row)
        # df_task_based_report = df_task_based_report.append(task_report, ignore_index=True)    
    report_summary.close()
    df_task_based_report.to_csv(f'{path_to_result}/task_based_report.csv', index = False)
    df_summary = pd.read_csv(f'{path_to_result}/results-summary.csv', 
    usecols=['totalCompletion%',
    'consumed_energy%','wasted_energy%','energy_per_completion%'])

    # print('\n\n'+ 10*'*'+'  Task_based Average Results '+10*'*')
    # print(df_task_based_report.mean())

    print('\n\n'+ 10*'*'+f'  Average Results of {config.scheduling_method}  '+10*'*')
    print(df_summary.mean())


