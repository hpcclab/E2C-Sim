'''
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

The main module reads tasks id, task_type_id, estimated_time, 
execution_time, and arrival_time. Then, add arrival events to the
Event_Queue. It also creates and starts machines. Finally, it reads all
events in the event_queue.event_list and call related function (add_task
or completing_task)

'''

from Machines import *


event_queue = EventQueue()
simulator = Simulator()

m1 = Machine(1, 'CPU')
m1.start()

Tasks = []
Tasks.append(Task(1,1,0.1 , 0.15, 0))
Tasks.append(Task(2,1,0.2 , 0.25, 0.1))
Tasks.append(Task(3,1,0.1 , 0.25, 0.35))

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
          "\tmachine#:" +str(m1.machine_id) +
          "\tCompletion_Time: "+str(task.completion_time))
        
        


