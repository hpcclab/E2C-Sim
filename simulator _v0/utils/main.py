'''
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

The main module reads tasks id, task_type_id, estimated_time, 
execution_time, and arrival_time. Then, add arrival events to the
Event_Queue. It also creates and starts machines. Finally, it reads all
events in the event_queue.event_list and call related function (add_task
or completing_task)

'''

from Machine import *
import Offload
import Config
from ComputingTier import *

config = Config.read_config()
event_queue = EventQueue()
simulator = Simulator()

#Config.process_config()

computing_tiers = []
machine_id = 0
all_machines = {}
for tier_item in config['computing_tiers']:
    
    tier = ComputingTier(tier_item['name'])
    print('\n'+80*'='+'\n\n Tier '+ tier.name + ' is created ...')
    
    for computing_unit_item in tier_item['computing_units']:
    #for computing_unit in config['computing_tier']:
    
        print( '\n\t'+50*'.'+'\n\t Attaching computing unit to the tier:'+
              '\n\t ID: '+ 
              str(computing_unit_item['id']) +
              '\n\t Total Energy: '+ 
              str(computing_unit_item['initial_energy'])+'[J]'+
              '\n\t Network Bandwidth: '+
              str(computing_unit_item['network_bandwidth'])+' [MB/Sec]')
              
        computing_unit = ComputingUnit (computing_unit_item['id'], 
                               computing_unit_item['initial_energy'],
                               computing_unit_item['power_limit'], 
                               computing_unit_item['network_bandwidth'])
        tier.add_computing_unit(computing_unit)
    
        
        print('\n\t Adding machines to the computing unit ====>>> ')
        for machine_item in computing_unit_item['machines']:    
            for no_of_machines in range(machine_item['replicas']):
                machine = Machine(machine_id, machine_item['machine_type'],
                            {'static_power':machine_item['dynamic_power'],
                             'dynamic_power':machine_item['static_power'],
                             'queue_length': machine_item['queue_length']})
                all_machines[machine.machine_id]= machine
                machine.start()
                computing_unit.add_machine(machine)
                machine_id +=1
    computing_tiers.append(tier)
        
computing_tiers[1].computing_units[0].machines


# cloud = Offload.Offload(100)
# cloud.start()

Tasks = []

with open('ArrivalTimes.txt','r') as data_file:
    
    for task in data_file:
        task = task.strip()
        task_details = [x.strip() for x in task.split(',')]
        #print(task_details)
        if task[0] == '#':            
            machine_types = [x.split('_')[-1] for x in task.split(',')[3:6]]            
        else:     
            task_id = int(task_details[0])
            task_type_id = int(task_details[1])
            arrival_time = float(task_details[2])
            estimated_time = {machine_types[0]: float(task_details[3]),
                              machine_types[1]: float(task_details[4]),
                              machine_types[2]: float(task_details[5]),
                              'CLOUD':float(task_details[6]) }
            execution_time = {machine_types[0]: float(task_details[7]),
                              machine_types[1]: float( task_details[8]),
                              machine_types[2]: float(task_details[9]),
                              'CLOUD':float(task_details[10])}
            
            Tasks.append(Task(task_id, task_type_id, estimated_time,
                              execution_time, arrival_time))

for task in Tasks:
    event = Event(task.arrival_time, 'arrival', task)
    event_queue.add_event(event)
count = 0
while event_queue.event_list:
    print(80*'=' + '\n\n Reading events from event queue ===>>>')
    event = event_queue.get_first_event()  
    simulator.set_current_time(event.time)
    
    if event.event_type =='arrival':
        task = event.event_details
        
        
        print('\n\t Task '+str(task.task_id) + ' arrived at '+
              str(simulator.get_current_time())+ ' sec'       )        
        
        # if task.task_id >= 3 and task.task_id <7:
        #     cloud.add_task(task)
        tier = computing_tiers[1]
        units = tier.computing_units
        no_of_units = len(units)
        unit_no = count % no_of_units
        unit = units[unit_no]
        no_of_machines = len(unit.machines)
        machine_no = count % no_of_machines
        machine = unit.machines[machine_no]
        print('\t task '+ str(task.task_id) + ' assigned to: '+
              ' \n\t\t tier: '+ tier.name +
              '\n\t\t computing unit: '+ str(unit.id) +
              '\n\t\t machine type: '+ machine.machine_type+ 
              '\n\t\t machine id : '+ str(machine.machine_id))
        machine.add_task(task)
        count +=1
        
    elif event.event_type =='completion':
       
        task = event.event_details
        machine = all_machines[event.event_details.mapped_machine_id]
        print('\n\t Task '+str(task.task_id) + ' completed at '+
              str(simulator.get_current_time())+ ' sec on :' +
              ' \n\t\t tier: '+ tier.name +
              '\n\t\t machine type: '+ machine.machine_type+ 
              '\n\t\t machine id : '+ str(machine.machine_id))
        
        machine.completing_task(event.event_details)
    # elif event.event_type =='completion_offloaded':
    #     cloud.completing_task(event.event_details)
    print('\n'+ 50*'.')
    for task in Tasks:
        
        print("  Task id = "+str(task.task_id)+ 
              '\t assigned to machine '+ str(task.mapped_machine_id) + 
              "\t status = "+ task.status)


        


