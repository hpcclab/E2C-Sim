
from utils.simulator import Simulator
from utils.machine import Machine
import utils.config as config
import  gui.simUi as gui

from PyQt5.QtWidgets import QApplication
import sys
import csv
import pandas as pd
from os import makedirs


workload_name = 'mini'
scenario = 'sc-2'
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


app = QApplication(sys.argv)   
view = gui.SimUi(workload_name, scenario, etc, workload_id)

view.show()
app.exec()
    
  

