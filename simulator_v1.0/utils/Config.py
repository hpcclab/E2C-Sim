
import json
from EventQueue import EventQueue
from MachineType import MachineType
from TaskType import TaskType
from Machine import Machine


event_queue = EventQueue()
machine_types = []
machines = []
task_types = []
tasks = []

current_time = 0.0 
episode = 5


with open(file='./config.json') as f:
    data = f.read()
# reconstructing the data as a dictionary
config = json.loads(data)

global_parameters = config['global_parameters']
queue_size = global_parameters[0]['queue_size']
batch_queue_size = global_parameters[0]['batch_queue_size']

machine_id = 1
for machine_type in config['machine_types']:
        type_id = machine_type['id']
        name = machine_type['name']
        power = machine_type['power']
        replicas = machine_type['replicas']
        type = MachineType(type_id, name, power, replicas)
        machine_types.append(type)
        for _ in range (replicas):                
                machine = Machine(machine_id, type, {} )
                machines.append(machine)
                machine_id +=1



for task_type in config['task_types']:
        _id = task_type['id']
        _name = task_type['name']
        _deadline = task_type['deadline']
        task_types.append(TaskType(_id, _name, _deadline))

def find_task_types(id):

        for type in task_types:
                if type.id == id:
                        return type
        return None
                


