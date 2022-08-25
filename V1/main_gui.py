
from utils.simulator import Simulator
from utils.machine import Machine
import utils.config as config
import  gui.simUi as gui

from PyQt5.QtWidgets import QApplication
import sys
import csv
import pandas as pd
from os import makedirs



heterogeneity_folder = 'homo'
scenario = 'default'
etc = 'etc-0'

workload_id = 1

config.init()

id = 0
for machine_type in config.machine_types:
    for r in range(1,machine_type.replicas+1):
        specs = {'power': machine_type.power, 'idle_power':machine_type.idle_power}
        machine = Machine(id,r, machine_type, specs)
        config.machines.append(machine)            
        id += 1

#path_to_result = f'./output/data/{heterogeneity_folder}/{etc}/{scenario}/{config.scheduling_method}'        
#makedirs(path_to_result, exist_ok = True)
app = QApplication(sys.argv)   
path_to_arrivals = './workloads/default/workload.csv'
path_to_etc = './task_machine_performance/default/etc.csv'
path_to_report = './output/data/default'
view = gui.SimUi(path_to_arrivals, path_to_etc, path_to_report)

view.show()
app.exec()

    


