from BaseTask import UrgencyLevel
import json
from EventQueue import EventQueue
from MachineType import MachineType
from TaskType import TaskType
from Machine import Machine
from Cloud import Cloud
import csv
import numpy as np


event_queue = EventQueue()
machine_types = []
machines = []
task_types = []
tasks = []


current_time = 0.0

no_of_machines = None

log = open('log.txt','w')
history = open('history-train.csv','w')
header = ['Action', 'Rewards', 'Gain', 'Loss']
history_writer = csv.writer(history)
history_writer.writerow(header)
with open(file='./config.json') as f:
    data = f.read()
# reconstructing the data as a dictionary
config = json.loads(data)

global_parameters = config['global_parameters']
queue_size = global_parameters[0]['queue_size']
batch_queue_size = global_parameters[0]['batch_queue_size']
scheduling_method = global_parameters[0]['scheduling_method']
gui = global_parameters[0]['gui']

battery = config['battery']
capacity = battery[0]['capacity']
total_energy = capacity * 3600   # capacity is in watt.hour while total energy is in joule
available_energy = total_energy

bandwidth = config['cloud'][0]['bandwidth']
latency = config['cloud'][0]['latency']
cloud = Cloud(bandwidth, latency)

machine_id = 1
for machine_type in config['machine_types']:
    type_id = machine_type['id']
    name = machine_type['name']
    power = machine_type['power']
    idle_power = machine_type['idle_power']
    replicas = machine_type['replicas']
    type = MachineType(type_id, name, power, replicas)
    machine_types.append(type)
    for _ in range(replicas):
        machine = Machine(machine_id, type, {'power':power, 'idle_power':idle_power})
        machines.append(machine)
        machine_id += 1

for task_type in config['task_types']:
    _id = task_type['id']
    _name = task_type['name']
    _urgency = task_type['urgency']
    if _urgency == 'best_effort':
        _urgency = UrgencyLevel.BESTEFFORT
    elif _urgency == 'urgent':
        _urgency = UrgencyLevel.URGENT
    _deadline = task_type['deadline']
    task_types.append(TaskType(_id, _name, _urgency,_deadline))

no_of_machines = len(machines)
def find_task_types(id):
    for type in task_types:
        if type.id == id:
            return type
    return None
