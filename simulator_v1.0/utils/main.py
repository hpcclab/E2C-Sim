import Config
from Task import Task
from Event import Event, EventTypes
from FCFS import FCFS


Tasks = []

with open('ArrivalTimes.txt','r') as data_file:
    
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
                              'CLOUD':float(task_details[6]) }
            execution_time = {machine_types[0]: float(task_details[7]),
                              machine_types[1]: float( task_details[8]),
                              machine_types[2]: float(task_details[9]),
                              'CLOUD':float(task_details[10])}
            
            type = Config.find_task_types(task_type_id)
            Tasks.append(Task(task_id, type, estimated_time,
                              execution_time, arrival_time))
for task in Tasks:
    event = Event(task.arrival_time, EventTypes.ARRIVING, task)
    Config.event_queue.add_event(event)

scheduler = FCFS()

while Config.event_queue.event_list :
    
    print(80*'=' + '\n\n Reading events from event queue ===>>>')
    event = Config.event_queue.get_first_event()  
    Config.current_time = event.time
    
    if event.event_type == EventTypes.ARRIVING:
        task = event.event_details
        
        print('\nTask '+str(task.id) + ' arrived at '+
              str(Config.current_time)+ ' sec'       )        
        
        scheduler.unlimited_queue.append(task)        
        scheduler.feed()
        assigned_machine = scheduler.schedule()
        if assigned_machine:
            assigned_machine.execute()
             
        
    elif event.event_type == EventTypes.COMPLETION:
       
        task = event.event_details
        machine = task.assigned_machine
        print('\n\t Task '+str(task.id) + ' completed at '+
              str(Config.current_time)+ ' sec on :' +            
              '\n\t\t machine type: '+ machine.type.name+ 
              '\n\t\t machine id : '+ str(machine.id))
        
        machine.terminate()
        scheduler.feed()
        assigned_machine = scheduler.schedule()
        if assigned_machine:           
            assigned_machine.execute()
   
    print('\n'+ 50*'.')
    
    for task in Tasks:        
        if task.assigned_machine != None:
            print("  Task id = "+str(task.id)+ 
                '\t assigned to '+ str(task.assigned_machine.type.name) + 
                 " " + str(task.assigned_machine.id) +
                "\t status = "+ task.status.name)
        else:
            print("  Task id = "+str(task.id)+ 
                '\t assigned to '+ str(task.assigned_machine) +
                "\t status = "+ task.status.name)