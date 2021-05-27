
import json

from MachineType import MachineType
from TaskType import TaskType


machine_types = []
machines = []
task_types = []
tasks = []
queue_size = None
current_time = 0.0 

with open(file='./config.json') as f:
    data = f.read()
# reconstructing the data as a dictionary
config = json.loads(data)

for machine_type in config['machine_types']:
        _id = machine_type['id']
        _name = machine_type['name']
        _power = machine_type['power']
        _replicas = machine_type['replicas']
        machine_types.append(MachineType(_id, _name, _power, _replicas))


for task_type in config['task_types']:
        _id = task_type['id']
        _name = task_type['name']
        task_types.append(TaskType(_id, _name))

global_parameters = config['global_parameters']
queue_size = global_parameters[0]['queue_size']
batch_queue_size = global_parameters[0]['batch_queue_size']
