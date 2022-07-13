
import pandas as pd
import numpy as np
import csv
from os import makedirs

from utils.simulator import Simulator
from utils.machine import Machine
import utils.config as config
from workload.generator import workloads_generator

from workload.workload import Workload
#from gui.gui_ali import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

workload_name = 'mini'
sc = 'sc-2'
etc_id = 0
etc = f'etc-{etc_id}'
workload_id = 1

        
config.init()            
path_to_result = f'./output/data/{workload_name}/{sc}/{etc}/{config.scheduling_method}'        
makedirs(path_to_result, exist_ok = True)
report_summary = open(f'{path_to_result}/results-summary.csv','w')
report_header = ['workload_id', 'total_no_of_tasks','mapped','cancelled','URG_missed','BE_missed','Completion%','xCompletion%','totalCompletion%','wasted_energy%','consumed_energy%','energy_per_completion%']
report = csv.writer(report_summary)
report.writerow(report_header) 

       
config.init()
m_id = 0
for machine_type in config.machine_types:
    for r in range(1,machine_type.replicas+1):
        specs = {'power': machine_type.power, 'idle_power':machine_type.idle_power}
        machine = Machine(m_id,r, machine_type, specs)
        config.machines.append(machine)            
        m_id += 1
    
simulation = Simulator(workload_name, sc, etc, workload_id) 
simulation.create_event_queue()
scheduler = config.get_scheduler()
simulation.set_scheduling_method(scheduler)        
simulation.run()           
row = simulation.report()   
report.writerows(row)        
report_summary.close()            
df_summary = pd.read_csv(f'{path_to_result}/results-summary.csv', 
usecols=['totalCompletion%',
'consumed_energy%','wasted_energy%'])
print('\n\n'+ 10*'*'+f'  <<{workload_name}>>||{sc} || {etc} --> {workload_id}: <<{config.scheduling_method}>> '+10*'*')
print(df_summary.mean())





