
"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022

"""

import json
import sys

from utils.memory import Memory
from utils.application import Application
from utils.event_queue import EventQueue
from utils.time import Time


def init(path_to_config='./config.json'):
    global memory, time, event_queue     
    global apps, apps_names
    global window
    global eviction_method 
    global path_to_workloads
    global log

    
    log = open('./output/log.txt','w')
    try:
        with open(path_to_config) as config:
            data = json.load(config)           
    except FileNotFoundError as fnf_err:
        print(fnf_err)            
        sys.exit()
    
    time = Time()
    event_queue = EventQueue()

    memory_size = data['memory'][0]['size']
    memory = Memory(memory_size)
    memory.init(memory_size)

    apps_data = data['applications'][0]
    apps = []
    apps_names = []

    for app_name, models in apps_data.items():
        app = Application(app_name, models['model_size'])
        apps.append(app)
        apps_names.append(app_name)

    window = data['global_parameters'][0]['window']
    eviction_method = data['global_parameters'][0]['eviction_method']
    path_to_workloads = data['environment_settings'][0]['path_to_workloads']

    



def find_app(app_name):
    founds = [app for app in apps if app.name == app_name]
    try:
        assert (len(founds) <= 1), f'ERROR[config.py -> find_app(app_name)] There are more than one app named as {app_name}'
        assert (len(founds) > 0 ), f'ERROR[config.py -> find_app(app_name)] No app is found with the name {app_name}'
    except  AssertionError as err:
        print(err)
        sys.exit()

    return founds[0]

