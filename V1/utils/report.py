import csv
import os
import utils.config as config

    
def report(path_to_reports, path_to_arrivals, scheduler, total_no_of_tasks, tasks, is_detailed = True):     
    path_to_report = f'{path_to_reports}/{scheduler.name}'        
    os.makedirs(path_to_report, exist_ok = True)        
    if is_detailed:  
        detailed_header = ['id','type','urgency','status','assigned_machine', 
                'arrival_time','execution_time','energy_usage','start_time',
                'completion_time','missed_time','deadline',
                'extended_deadline']
        
        if config.gui:
            try:

                files = [x for x in os.listdir(f'{path_to_report}/') if x.endswith('csv')]
            except:
                files = []
            new_file = 'detailed.csv'
            i=1
            while files and (new_file in files):
                new_file = f'detailed-copy({i}).csv'
                i+=1
        else:

            workload_id = path_to_arrivals.split('/')[-1].split('-')[-1].split('.')[0]
            new_file = f'detailed-{workload_id}.csv'

        detailed = open(f'{path_to_report}/{new_file}','w')
        detailed_writer = csv.writer(detailed)
        detailed_writer.writerow(detailed_header)

        for task in tasks:
            if task.assigned_machine == None:
                assigned_machine = None
            else:
                assigned_machine = f'{task.assigned_machine.type.name}-{task.assigned_machine.replica_id}'
            
            detailed_row = [
                task.id,task.type.name,task.urgency.name,
                task.status.name,assigned_machine, task.arrival_time,
                task.execution_time,task.energy_usage,task.start_time,
                task.completion_time,task.missed_time,
                task.deadline - task.devaluation_window, task.deadline]       

            detailed_writer.writerow(detailed_row) 
        detailed.close()           

    total_assigned_tasks = 0
    total_completion = 0
    total_xcompletion = 0
    missed_urg = 0
    missed_be = 0
    total_wasted_energy = 0         

    for machine in config.machines:
        total_assigned_tasks += machine.stats['assigned_tasks']
        total_completion += machine.stats['completed_tasks']
        total_xcompletion += machine.stats['xcompleted_tasks']
        total_wasted_energy += machine.stats['wasted_energy']
        missed_urg += machine.stats['missed_URG_tasks']
        missed_be += machine.stats['missed_BE_tasks']

        completed_percent = 0
        xcompleted_percent = 0                        
        energy_percent = 100 * (machine.stats['energy_usage'] / config.total_energy)
        wasted_energy_percent = 100 * (machine.stats['wasted_energy'] / config.total_energy)
        if machine.stats['assigned_tasks'] != 0:
            completed_percent = 100 * (machine.stats['completed_tasks'] / machine.stats['assigned_tasks'])
            xcompleted_percent = 100 *(machine.stats['xcompleted_tasks'] / machine.stats['assigned_tasks'])

        s = '\nMachine: {:} (id#{:})  \n\t%Completion: {:2.1f} #: {:}\n\t%XCompletion:{:2.1f} #: {:}\n\t#Missed URG:{:1.2f}\n\tMissed BE:{:}\n\t%Energy: {:2.1f}\n\t%Wasted Energy: {:2.1f} '.format(
            machine.type.name,machine.id,
            completed_percent, machine.stats['completed_tasks'],
            xcompleted_percent, machine.stats['xcompleted_tasks'],
            machine.stats['missed_URG_tasks'],
            machine.stats['missed_BE_tasks'],
            energy_percent,
            wasted_energy_percent)
        
        
                    
        # if self.verbosity <= 3 :
        #print(s)
        config.log.write(s)

    total_completion_percent = 100 * (total_completion / total_no_of_tasks)
    total_xcompletion_percent = 100 * (total_xcompletion / total_no_of_tasks)
    total_missed_be_percent = 100 * ((missed_be) / total_no_of_tasks)
    total_missed_urg_percent = 100 * ((missed_urg) / total_no_of_tasks)
    total_wasted_energy_percent = 100 * (total_wasted_energy / config.total_energy)
    s = '\n%Total Completion: {:2.1f}'.format(total_completion_percent)
    s += '\n%Total xCompletion: {:2.1f}'.format(total_xcompletion_percent)
    s += '\n%Total Missed BE: {:2.1f}'.format(total_missed_be_percent)
    s += '\n%Total Missed URG: {:2.1f}'.format(total_missed_urg_percent)
    s += '\n%deferred: {:2.1f}'.format(len(scheduler.stats['deferred']))
    s += '\n%dropped: {:2.1f}'.format(len(scheduler.stats['dropped']))
    # if self.verbosity <= 3:
    print(s)
    config.log.write(s)

    # d = {}
    # for task_type in config.task_types:
    #     for machine in config.machines:
    #         d [f'{task_type.name}_assignedto{machine.type.name}_{machine.replica_id}'] = 0
    #         d[f'{task_type.name}completed{machine.type.name}_{machine.replica_id}']=0
    #         d[f'{task_type.name}xcompleted{machine.type.name}_{machine.replica_id}'] = 0
    #         d[f'{task_type.name}missed{machine.type.name}_{machine.replica_id}']=0
    #         d[f'{task_type.name}energy{machine.type.name}_{machine.replica_id}']=0
    #         d[f'{task_type.name}wasted-energy{machine.type.name}_{machine.replica_id}']=0

    row = []
    consumed_energy = config.total_energy - config.available_energy
    no_of_completed_task = total_no_of_tasks*0.01*(total_completion_percent+total_xcompletion_percent)
    if no_of_completed_task != 0:
        energy_per_completion = consumed_energy / no_of_completed_task
        energy_per_completion = 100*(energy_per_completion/ config.total_energy)
    elif consumed_energy != 0 and no_of_completed_task == 0:
        energy_per_completion = float('inf')
    else:
        energy_per_completion = 0.0

    row.append(
        [path_to_arrivals,total_no_of_tasks ,
        total_assigned_tasks, len(scheduler.stats['dropped']),
        missed_urg,
        missed_be,
        total_completion_percent, total_xcompletion_percent,
        total_completion_percent+total_xcompletion_percent,
        total_wasted_energy_percent,
        100*(consumed_energy/config.total_energy),            
        energy_per_completion ])       
    config.log.close()
    #print(row)
    return row