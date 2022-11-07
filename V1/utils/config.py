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

def create_deadline(deadline_value):
    deadline = 45.0
    try:
        if deadline_value < 0:
            print("WARNING: Value for deadline should not be negative")
        if deadline_value != 0:
            deadline = abs(float(deadline_value))
        else:
            print("ERROR: Value for deadline cannot be 0. 45.0 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for deadline. 45.0 will be set instead.")
        deadline = 45.0
    return deadline

def create_idle_power(value):
    idle_power = 5
    try:
        if value < 0:
            print("WARNING: Value for idle_power should not be negative")
        if value != 0:
            idle_power = abs(int(value))
        else:
            print("ERROR: Value for idle_power cannot be 0. 5 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for idle_power. 5 will be set instead.")
        idle_power = 5
    return idle_power

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
        deadline = create_deadline(task_type['deadline'])
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
        power = create_power(machine_type['power'])
        idle_power = create_idle_power(machine_type['idle_power'])
        replicas = create_replicas(machine_type['replicas'])
        type = MachineType(id, name, power,idle_power, replicas)
        no_of_machines += replicas
        machine_types.append(type)
        machine_type_names.append(name)  
    return machine_types, machine_type_names, no_of_machines

def create_power(value):
    power = 50
    try:
        if value < 0:
            print("WARNING: Value for power should not be negative")
        if value != 0:
            power = abs(int(value))
        else:
            print("ERROR: Value for power cannot be 0. 50 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for power. 50 will be set instead.")
        power = 50
    return power

def create_replicas(value):
    replicas = 1
    try:
        if value < 0:
            print("WARNING: Value for replicas should not be negative")
        if value != 0:
            replicas = abs(int(value))
        else:
            print("ERROR: Value for replicas cannot be 0. 1 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for replicas. 1 will be set instead.")
        replicas = 1
    return replicas


    



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
    if (str(scheduler) == 'EE' or 'MM' or 'FEE' or 'MSD' or 'MMU' or 'FCFS' or 'MECT' or 'MEET' ):
        scheduling_method = scheduler
    else:
        print('ERROR: Invalid Scheduling Method. FCFS will be set instead.')
        scheduling_method = 'FCFS'

def get_scheduler():
    global scheduling_method
    return scheduling_method


def set_machine_queue_size(size):
    global machine_queue_size
    machine_queue_size = 3
    try:
        if size < 0:
            print("WARNING: Value for machine_queue_size should not be negative")
        if size != 0:
            machine_queue_size = abs(int(size))
        else:
            print("ERROR: Value for machine_queue_size cannot be 0. 3 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for machine_queue_size. 3 will be set instead.")
        machine_queue_size = 3


def get_machine_queue_size():
    global machine_queue_size
    return machine_queue_size

def set_capacity(capacity_value):
    global capacity
    global total_energy
    global available_energy
    capacity = 500.0
    try:
        if capacity_value < 0:
            print("WARNING: Value for capacity should not be negative.")
        if capacity_value != 0:
            capacity = abs(int(capacity_value))
        else:
            print("ERROR: Value for capacity cannot be 0. 500.0 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for capacity. 500.0 will be set instead.")
    total_energy = capacity * 3600
    available_energy = total_energy

def set_batch_queue_size(value):
    global batch_queue_size
    batch_queue_size = 3
    try:
        if value < 0:
            print("WARNING: Value for batch_queue_size should not be negative.")
        if value != 0:
            batch_queue_size = abs(int(value))
        else:
            print("ERROR: Value for batch_queue_size cannot be 0. 3 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for batch_queue_size. 3 will be set instead.")

def set_fairness_factor(value):
    global fairness_factor
    fairness_factor = 1.0
    try:
        if value < 0:
            print("WARNING: Value for fairness_factor should not be negative.")
        if value != 0:
            fairness_factor = abs(float(value))
        else:
            print("ERROR: Value for fairness_factor cannot be 0. 1.0 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for fairness_factor. 1.0 will be set instead.")

def set_bandwidth(value):
    global bandwidth
    bandwidth = 15000.0
    try:
        if value < 0:
            print("WARNING: Value for bandwidth should not be negative.")
        if value != 0:
            bandwidth = abs(float(value))
        else:
            print("ERROR: Value for bandwidth cannot be 0. 15000.0 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for bandwidth. 15000.0 will be set instead.")

def set_network_latency(value):
    global network_latency
    network_latency = .015
    try:
        if value < 0:
            print("WARNING: Value for network_latency should not be negative.")
        if value != 0:
            network_latency = abs(float(value))
        else:
            print("ERROR: Value for network_latency cannot be 0. 0.015 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for network_latency. 0.015 will be set instead.")

def set_gui(value):
    global gui
    gui = 1
    try:
        if value < 0:
            print("WARNING: Value for gui should not be negative.")
        if value != 0:
            gui = abs(float(value))
        else:
            print("ERROR: Value for gui cannot be 0. 1 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for gui. 1 will be set instead.")

def set_verbosity(value):
    global verbosity
    verbosity = 3
    try:
        if value < 0:
            print("WARNING: Value for verbosity should not be negative.")
        if value != 0:
            verbosity = abs(float(value))
        else:
            print("ERROR: Value for verbosity cannot be 0. 3 will be set instead.")
    except ValueError as val_err:
        print("ERROR: Invalid value for verbosity. 3 will be set instead.")

def init():
    global event_queue
    global time
    global machines, machine_types, machine_type_names
    global task_types, task_type_names
    global cloud

    global capacity
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

    set_capacity(data['battery'][0]['capacity'])

    set_machine_queue_size(data['parameters'][0]['machine_queue_size'])
    # machine_queue_size = int(data['parameters'][0]['machine_queue_size'])
    set_batch_queue_size(data['parameters'][0]['batch_queue_size'])     
    set_fairness_factor(data['parameters'][0]['fairness_factor'])
    set_bandwidth(data['cloud'][0]['bandwidth'])
    set_network_latency(data['cloud'][0]['network_latency'])

    set_scheduler(data['parameters'][0]['scheduling_method'])
    

    settings = data['settings'][0] 
    set_gui(settings['gui']) 
    set_verbosity(settings['verbosity'])
    path_to_output = settings['path_to_output']
    path_to_workload = settings['path_to_workload']

    try:
        log = open(f"{path_to_output}/log.txt",'w')
    except OSError as err:
        print(err)
        path_to_output = "./output"

    try:
        log = open(f'{path_to_workload}/log.txt', 'w')
    except OSError as err:
        print(err)
        path_to_workload = '.workloads'

    
    




