import Config
from Task import Task
from Event import Event, EventTypes
from FCFS import FCFS
from MM import MM
from MSD import MSD
from MMU import MMU
from RLS import RLS
#from MIN import Min1
#from PhaseMIN1 import PhaseMIN1
#from PhaseMIN2 import PhaseMIN2

from tqdm import tqdm 
import csv

out = open('./results/RLS/results-summary.csv','w')
header = ['Episode', 'total_no_of_tasks','mapped', 'offloaded','cancelled','Completion%','xCompletion%','URG_missed','BE_missed','available_energy']
writer = csv.writer(out)
writer.writerow(header)
for i in range(100,130):
    
    Tasks = []
    Config.event_queue.reset()
    Config.current_time = 0.0
    Config.available_energy = Config.total_energy
    Config.cloud.reset()
    for machine in Config.machines:
        machine.reset()
    
    s = '\n\n'+ 15 * '='+' EPISODE#'+str(i)+' '+ 15 * '='
    Config.log.write(s)
    print(s)
    with open('./Episodes/ArrivalTimes/ArrivalTimes-'+str(i)+'.txt', 'r') as data_file:
    # with open('./ArrivalTimes.txt', 'r') as data_file:
        for task in data_file:
            task = task.strip()
            task_details = [x.strip() for x in task.split(',')]

            if task[0] == '#':
                machine_types = [x.split('_')[-1] for x in task.split(',')[4:6]]
            else:
                task_id = int(task_details[0])
                task_type_id = int(task_details[1])
                task_size = float(task_details[2])
                arrival_time = float(task_details[3])
                # estimated_time = {machine_types[0]: float(task_details[3]),
                #                 machine_types[1]: float(task_details[4]),                              
                #                 'CLOUD': float(task_details[5])}
                execution_time = {machine_types[0]: float(task_details[4]),
                                machine_types[1]: float(task_details[5]),                              
                                'CLOUD': float(task_details[6])}

                type = Config.find_task_types(task_type_id)
                # Tasks.append(Task(task_id, type, estimated_time,
                #                 execution_time, arrival_time))
                Tasks.append(Task(task_id, type,task_size,
                                execution_time, arrival_time))                
    for task in Tasks:
        event = Event(task.arrival_time, EventTypes.ARRIVING, task)
        Config.event_queue.add_event(event)
    total_no_of_tasks = len(Tasks)
    pbar = tqdm(total=total_no_of_tasks)
    scheduler = RLS(total_no_of_tasks)
    #scheduler = FCFS(total_no_of_tasks)
    #scheduler = MM(total_no_of_tasks)
    #scheduler = MSD(total_no_of_tasks)
    #scheduler = MMU(total_no_of_tasks)
    arrival_count = 0
    while Config.event_queue.event_list and Config.available_energy >0:
        
        event = Config.event_queue.get_first_event() 
        task = event.event_details   
        Config.current_time = event.time
        s = '\nTask:{} \t\t {}  @time:{}'.format(
                task.id, event.event_type.name, event.time)
        Config.log.write(s)
        #print(s)
        
        for machine in Config.machines:
            #print(machine.type.name, Config.current_time)
            idle_time_interval = Config.current_time - machine.idle_time

            if idle_time_interval >0:
                idle_energy_consumption = machine.specs['idle_power'] * (idle_time_interval/3600.0)
                machine.idle_time = Config.current_time
            else:
                idle_energy_consumption = 0.0 
            machine.stats['energy_usage'] += idle_energy_consumption
            Config.available_energy -= idle_energy_consumption
            s = '\nmachine {} @{}\n\tidle_time:{}\n\tidle_time_interval:{}\n\tidle power consumption: {} '.format(
                 machine.id, Config.current_time, machine.idle_time, idle_time_interval, idle_energy_consumption)
            Config.log.write(s)
            #print(s)
            

        

        
        if event.event_type == EventTypes.ARRIVING:            
            pbar.update(1)
            scheduler.unlimited_queue.append(task)
            scheduler.feed()       
            assigned_machine = scheduler.schedule()
            

        elif event.event_type == EventTypes.DEFERRED:               
            scheduler.feed()       
            assigned_machine = scheduler.schedule()
            if assigned_machine == -1:
                break
        
        elif event.event_type == EventTypes.COMPLETION:        
            machine = task.assigned_machine                 
            machine.terminate(task)
            scheduler.feed() 
            assigned_machine = scheduler.schedule()

        elif event.event_type == EventTypes.OFFLOADED:        
                     
            Config.cloud.terminate(task)
            scheduler.feed() 
            assigned_machine = scheduler.schedule()
                
        elif event.event_type == EventTypes.DROPPED_RUNNING_TASK:
                
            machine = task.assigned_machine        
            machine.drop()
            scheduler.feed()      
            assigned_machine = scheduler.schedule()
    scheduler.done = True
    scheduler.save('model.h5')
    pbar.close()
    header = ['id', 'type', 'size', 'urgency','status', 'assigned_machine',
    'arrival_time','execution_time','start_time', 'completion_time', 'deadline',
    'extended_deadline']
    with open('./results/RLS/results-'+ str(i)+'.csv','w') as results:
        results_writer = csv.writer(results)
        results_writer.writerow(header)
        for task in Tasks:
            if task.assigned_machine == None:
                assigned_machine = None
            else:
                assigned_machine = task.assigned_machine.type.name
            row = [task.id, task.type.name, task.task_size, task.urgency.name, 
            task.status.name, assigned_machine, task.arrival_time,task.execution_time,
             task.start_time, task.completion_time, task.deadline,
              task.deadline + task.devaluation_window]
            results_writer.writerow(row)
        


    #scheduler.save('model.h5')
    total_assigned_tasks = 0    
    total_completion = 0
    total_xcompletion = 0
    missed_urg = 0 
    missed_be = 0

    s = 'Scheduler Summary:\n\tTotal# of Tasks: {:}\n\t#Mapped: {:}\n\t#Cancelled: {:}\n\t#Offloaded: {:}\n\tDeferred: {:}'.format(
        total_no_of_tasks,len(scheduler.stats['mapped']),
        len(scheduler.stats['dropped']), len(scheduler.stats['offloaded']),
        len(scheduler.stats['deferred'])
    )
    print(s)
    Config.log.write(s)
    for machine in Config.machines:
        total_assigned_tasks += machine.stats['assigned_tasks']
        total_completion += machine.stats['completed_tasks']
        total_xcompletion += machine.stats['xcompleted_tasks']
        missed_urg += machine.stats['missed_URG_tasks']
        missed_be += machine.stats['missed_BE_tasks']

        if machine.stats['assigned_tasks'] != 0 :
            completed_percent = machine.stats['completed_tasks'] / machine.stats['assigned_tasks']
            xcompleted_percent = machine.stats['xcompleted_tasks'] / machine.stats['assigned_tasks']
            energy_percent = machine.stats['energy_usage'] / Config.total_energy
            s = '\nMachine: {:} (id#{:})  \n\t%Completion: {:2.1f} #: {:}\n\t%XCompletion:{:2.1f} #: {:}\n\t#Missed URG:{:1.2f}\n\tMissed BE:{:}\n\t%Energy: {:2.1f} '.format(
                machine.type.name,machine.id,
                100*completed_percent, machine.stats['completed_tasks'],
                100*xcompleted_percent, machine.stats['xcompleted_tasks'],
                machine.stats['missed_URG_tasks'],
                machine.stats['missed_BE_tasks'],
                100*energy_percent)
            print(s)
            Config.log.write(s)
    no_of_offloaded_tasks = Config.cloud.stats['offloaded_tasks']
    total_completion += Config.cloud.stats['completed_tasks']
    total_xcompletion += Config.cloud.stats['xcompleted_tasks']
    if no_of_offloaded_tasks != 0:
        percentage_offloaded_completed = 100 * Config.cloud.stats['completed_tasks'] / Config.cloud.stats['offloaded_tasks']
        percentage_offloaded_xcompleted = 100 * Config.cloud.stats['xcompleted_tasks'] / Config.cloud.stats['offloaded_tasks']
    else:
        percentage_offloaded_completed = 0
        percentage_offloaded_xcompleted = 0

    s = '\n Cloud:   \n\t#offloaded:{:}\n\t%Completion: {:2.1f}\n\t%XComplettion:{:2.1f}\n\t#Missed-URG:{:},\n\t#Missed-BE:{:}'.format(
        Config.cloud.stats['offloaded_tasks'],
        percentage_offloaded_completed,  
        percentage_offloaded_xcompleted,
        Config.cloud.stats['missed_URG_tasks'], Config.cloud.stats['missed_BE_tasks']
    )
    print(s)
    Config.log.write(s)
    total_completion_percent = 100* (total_completion / total_no_of_tasks)
    total_xcompletion_percent = 100* (total_xcompletion / total_no_of_tasks)
    s = '\n%Total Completion: {:2.1f}'.format(total_completion_percent)
    s += '\n%Total xCompletion: {:2.1f}'.format(total_xcompletion_percent)
    s += '\n%deferred: {:2.1f}'.format(len(scheduler.stats['deferred']))
    s += '\n%dropped: {:2.1f}'.format(len(scheduler.stats['dropped']))
    s += '\n%offloaded: {:2.1f}'.format(len(scheduler.stats['offloaded']))
    row = []
    
    row.append([i,total_no_of_tasks ,total_assigned_tasks, Config.cloud.stats['offloaded_tasks'],len(scheduler.stats['dropped']),
    total_completion_percent, total_xcompletion_percent,missed_urg, missed_be, Config.available_energy])
    writer.writerows(row)
    

    print(s)
    Config.log.write(s)

    
    
    s = '\nAvailable Energy: {} '.format(Config.available_energy)
    print(s)
    Config.log.write(s)

    for task in Tasks:
        if task.assigned_machine is not None:
            s = "\n  Task id = {}\t assigned to {}\t status ={} ".format(task.id,task.assigned_machine.id,
                    task.status.name)
            Config.log.write(s)
            
        else:
            s = "\n  Task id ={} \t NOT assigned:\t status ={} ".format(task.id,task.status.name)
            Config.log.write(s)
    Config.log.write(60*'=')
out.close() 
Config.log.close()
Config.history.close()     