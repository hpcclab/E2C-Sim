"""
Author: Ali Mokhtari
Created on Jan. 27, 2021.

This module reads configuration parameters from the json file. 

"""
import json


def read_config(path='./config.txt'):
    # This function read configuration parameters from the json file 
    # located in path
    with open(path) as f:
        data = f.read()
        # reconstructing the data as a dictionary
    config = json.loads(data)

    return config


def process_config():
    computing_tiers = []
    machine_id = 0
    all_machines = {}
    for tier_item in read_config()['computing_tiers']:

        tier = ComputingTier(tier_item['name'])
        print('\n' + 80 * '=' + '\n\n Tier ' + tier.name + ' is created ...')

        for computing_unit_item in tier_item['computing_units']:

            print('\n\t' + 50 * '.' + '\n\t Attaching computing unit to the tier:' +
                  '\n\t ID: ' +
                  str(computing_unit_item['id']) +
                  '\n\t Total Energy: ' +
                  str(computing_unit_item['initial_energy']) + '[J]' +
                  '\n\t Network Bandwidth: ' +
                  str(computing_unit_item['network_bandwidth']) + ' [MB/Sec]')

            computing_unit = ComputingUnit(computing_unit_item['id'],
                                           computing_unit_item['initial_energy'],
                                           computing_unit_item['power_limit'],
                                           computing_unit_item['network_bandwidth'])
            tier.add_computing_unit(computing_unit)

            print('\n\t Adding machines to the computing unit ====>>> ')
            for machine_item in computing_unit_item['machines']:
                for no_of_machines in range(machine_item['replicas']):
                    machine = Machine(machine_id, machine_item['machine_type'],
                                      {'static_power': machine_item['dynamic_power'],
                                       'dynamic_power': machine_item['static_power'],
                                       'queue_length': machine_item['queue_length']})
                    all_machines[machine.machine_id] = machine
                    machine.start()
                    computing_unit.add_machine(machine)
                    machine_id += 1
        computing_tiers.append(tier)

    computing_tiers[1].computing_units[0].machines

    Tasks = []

    with open('ArrivalTimes.txt', 'r') as data_file:

        for task in data_file:
            task = task.strip()
            task_details = [x.strip() for x in task.split(',')]
            if task[0] == '#':
                machine_types = [x.split('_')[-1] for x in task.split(',')[3:6]]
            else:
                task_id = int(task_details[0])
                task_type_id = int(task_details[1])
                arrival_time = float(task_details[2])
                estimated_time = {machine_types[0]: float(task_details[3]),
                                  machine_types[1]: float(task_details[4]),
                                  machine_types[2]: float(task_details[5]),
                                  'CLOUD': float(task_details[6])}
                execution_time = {machine_types[0]: float(task_details[7]),
                                  machine_types[1]: float(task_details[8]),
                                  machine_types[2]: float(task_details[9]),
                                  'CLOUD': float(task_details[10])}

                Tasks.append(Task(task_id, task_type_id, estimated_time,
                                  execution_time, arrival_time))
