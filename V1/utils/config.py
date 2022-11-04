"""
Authors: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 24, 2022

Description:


"""
import json
import sys

from utils.time import Time
from utils.event_queue import EventQueue
from utils.task_type import TaskType, UrgencyLevel
from utils.machine_type import MachineType


def load_config(path_to_config = './config.json'):
    try:
        f = open(path_to_config)
    except FileNotFoundError as fnf_err:
        print(fnf_err)
        sys.exit()
    data = f.read()
    f.close()
    data = json.loads(data)
    return data

def create_task_types(task_types_info):
    task_types = []
    task_type_names = []
    for id, task_type in enumerate(task_types_info):
        #id = task_type['id']
        name = task_type['name']
        urgency = task_type['urgency'].lower()
        if urgency == 'best_effort':
            urgency = UrgencyLevel.BESTEFFORT
        elif urgency == 'urgent':
            urgency = UrgencyLevel.URGENT
        deadline = float(task_type['deadline'])
        task_types.append(TaskType(id, name, urgency,deadline))
        task_type_names.append(name)
    return task_types, task_type_names

def create_machine_types(machines_info):
    
    machine_types = []
    machine_type_names = [] 
    no_of_machines = 0   
    
    for id, machine_type in enumerate(machines_info):
        #type_id = machine_type['type_id']        
        name = machine_type['name']
        power = int(machine_type['power'])
        idle_power = int(machine_type['idle_power'])
        replicas = int(machine_type['replicas'])
        type = MachineType(id, name, power,idle_power, replicas)
        no_of_machines += replicas
        machine_types.append(type)
        machine_type_names.append(name)
        
        
    return machine_types, machine_type_names, no_of_machines

def find_task_type(task_type_name):
    try:
        for task_type in task_types:            
                if task_type.name == task_type_name:
                    return task_type
        raise Exception ('ERROR: The task type id does not exist in config.task_types')
    except  ValueError as err:
        print(err)

def set_scheduler(scheduler):
    global scheduling_method
    scheduling_method = scheduler

def get_scheduler():
    global scheduling_method
    return scheduling_method

def set_machine_queue_size(size):
    global machine_queue_size
    machine_queue_size = machine_queue_size

def get_machine_queue_size():
    global machine_queue_size
    return machine_queue_size

def init():
    global event_queue
    global time
    global machines, machine_types, machine_type_names
    global task_types, task_type_names
    global cloud

    global settings    
    global scheduling_method
    global fairness_factor
    global total_energy, available_energy    
    global machine_queue_size, batch_queue_size
    global no_of_machines
    global bandwidth, network_latency
    global gui
    
    global log
    global path_to_output
    global path_to_workload
    global verbosity
    
    data = load_config()
    
    # add verbosity and gui setting to config.py

    time = Time()
    event_queue = EventQueue()

    # add try/catch for input validation

    task_types, task_type_names = create_task_types(data['task_types'])
    machine_types, machine_type_names, no_of_machines = create_machine_types(data['machines'])
    machines = []

    capacity = float(data['battery'][0]['capacity'])
    total_energy = capacity * 3600
    available_energy = total_energy

    machine_queue_size = int(data['parameters'][0]['machine_queue_size'])
    batch_queue_size = int(data['parameters'][0]['batch_queue_size'])     
    fairness_factor = float(data['parameters'][0]['fairness_factor'])
    bandwidth = float(data['cloud'][0]['bandwidth'])
    network_latency = float(data['cloud'][0]['network_latency'])

    if (data['parameters'][0]['scheduling_method'] == 'EE' or 'MM' or 'FEE' or 'MSD' or 'MMU' or 'FCFS' or 'MECT' or 'MEET' ):
        set_scheduler(data['parameters'][0]['scheduling_method'])
    else:
        print('Invalid Scheduling Method')
        set_scheduler('FCFS')


    settings = data['settings'][0] 
    gui = int(settings['gui']) 
    verbosity = int(settings['verbosity'])
    path_to_output = settings['path_to_output']
    path_to_workload = settings['path_to_workload']

    try:
        log = open(f"{path_to_output}/log.txt",'w')
    except OSError as err:
        print(err)

    
    




