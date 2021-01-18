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
import Config

Config.init()
event_queue = EventQueue()
simulator = Simulator()

m1 = Machine(1, 'CPU')
m1.start()

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
                              machine_types[2]: float(task_details[5])}
            execution_time = {machine_types[0]: float(task_details[6]),
                              machine_types[1]: float( task_details[7]),
                              machine_types[2]: float(task_details[8])}
            
            Tasks.append(Task(task_id, task_type_id, estimated_time,
                              execution_time, arrival_time))

for task in Tasks:
    event = Event(task.arrival_time, 'arrival', task)
    event_queue.add_event(event)

while event_queue.event_list:
    print(20*"-")
    event = event_queue.get_first_event()
    print(event.event_type, ' task id -->',event.event_details.task_id)
    
    simulator.set_current_time(event.time)
    print("current time = "+ str(simulator.get_current_time()))    
    
    if event.event_type =='arrival':
        m1.add_task(event.event_details)  
    elif event.event_type =='completion':
        m1.completing_task()
    
    for task in Tasks:
        print("task id = "+str(task.task_id)+ " Status = "+ task.status)

print(3*'\n'+ 40*"*")
for task in m1.completion_queue:
    print("task#:" + str(task.task_id) +
          "\t \t machine#:" +str(m1.machine_id) +
          "\t \t Completion_Time: "+str(round(task.completion_time,3)))
        
        


