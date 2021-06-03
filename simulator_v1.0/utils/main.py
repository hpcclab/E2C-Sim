import Config
from Task import Task
from Event import Event, EventTypes
from FCFS import FCFS
from MIN import Min1
from PhaseMIN1 import PhaseMIN1
from PhaseMIN2 import PhaseMIN2

# The following creates the GUI window
import tkinter as tk
window = tk.Tk()
window.title("Scheduler")
window.geometry('1000x1000')

tArrivalTime = tk.Text(window, height=10, width=100)
tCompletionTime = tk.Text(window, height=10, width=100)
tTaskStatus = tk.Text(window, height=10, width=100)

lbl1 = tk.Label(window, text="Task Arrival Times")
lbl1.config(font=("Courier", 14))
lbl2 = tk.Label(window, text="Task Completion Times")
lbl2.config(font=("Courier", 14))
lbl3 = tk.Label(window, text="Task Statuses")
lbl3.config(font=("Courier", 14))

b = tk.Button(window, text="Exit", command=window.destroy)

lbl1.pack()
tArrivalTime.pack()
lbl2.pack()
tCompletionTime.pack()
lbl3.pack()
tTaskStatus.pack()
b.pack()
# end of GUI window code

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

            type = Config.find_task_types(task_type_id)
            Tasks.append(Task(task_id, type, estimated_time,
                              execution_time, arrival_time))
for task in Tasks:
    event = Event(task.arrival_time, EventTypes.ARRIVING, task)
    Config.event_queue.add_event(event)

'''
# Code for 2 phase scheduling: Work in progress
scheduler1 = PhaseMIN1()
scheduler2 = PhaseMIN2()

while Config.event_queue.event_list:

    print(80 * '=' + '\n\n Reading events from event queue ===>>>')
    event = Config.event_queue.get_first_event()
    Config.current_time = event.time

    if event.event_type == EventTypes.ARRIVING:
        task = event.event_details

        print('\nTask ' + str(task.id) + ' arrived at ' +
              str(Config.current_time) + ' sec')

        scheduler1.unlimited_queue.append(task)
        scheduler1.feed()
        minList = scheduler1.schedule()
        print(minList)
        assigned_machine = scheduler2.schedule(minList)
        if assigned_machine:
            assigned_machine.execute()

    elif event.event_type == EventTypes.COMPLETION:

        task = event.event_details
        machine = task.assigned_machine
        print('\n\t Task ' + str(task.id) + ' completed at ' +
              str(Config.current_time) + ' sec on :' +
              '\n\t\t machine type: ' + machine.type.name +
              '\n\t\t machine id : ' + str(machine.id))

        machine.terminate()
        scheduler1.feed()
        assigned_machine = scheduler1.schedule()
        if assigned_machine:
            assigned_machine.execute()

    print('\n' + 50 * '.')

    for task in Tasks:
        if task.assigned_machine is not None:
            print("  Task id = " + str(task.id) +
                  '\t assigned to ' + str(task.assigned_machine.type.name) +
                  " " + str(task.assigned_machine.id) +
                  "\t status = " + task.status.name)
        else:
            print("  Task id = " + str(task.id) +
                  '\t assigned to ' + str(task.assigned_machine) +
                  "\t status = " + task.status.name)
'''
# To change scheduling method, change what scheduler variable is set to
scheduler = Min1()
while Config.event_queue.event_list:

    print(80 * '=' + '\n\n Reading events from event queue ===>>>')
    event = Config.event_queue.get_first_event()
    Config.current_time = event.time

    if event.event_type == EventTypes.ARRIVING:
        task = event.event_details

        # the next three lines format text to be added to the window and then it adds it into the "Task Arrival Times"
        # Section.
        string = ('Task ' + str(task.id) + ' arrived at ' +
                  str(Config.current_time) + ' sec\n')
        tArrivalTime.insert(tk.END, string)

        scheduler.unlimited_queue.append(task)
        scheduler.feed()
        assigned_machine = scheduler.schedule()
        if assigned_machine:
            assigned_machine.execute()

    elif event.event_type == EventTypes.COMPLETION:

        task = event.event_details
        machine = task.assigned_machine
        string = ('\n\t Task ' + str(task.id) + ' completed at ' +
                  str(Config.current_time) + ' sec on :' +
                  '\n\t\t machine type: ' + machine.type.name +
                  '\n\t\t machine id : ' + str(machine.id))
        print(string)

        # the next five lines format text to be added to the window and then it adds it into the "Task Completion
        # Time" Section.
        string = ('Task ' + str(task.id) + ' completed at ' +
                  str(round(Config.current_time, 3)) + ' sec on' +
                  ' machine type: ' + machine.type.name +
                  ', and machine id: ' + str(machine.id) + "\n")
        tCompletionTime.insert(tk.END, string)

        machine.terminate()
        scheduler.feed()
        assigned_machine = scheduler.schedule()
        if assigned_machine:
            assigned_machine.execute()

    print('\n' + 50 * '.')

    for task in Tasks:
        if task.assigned_machine is not None:
            print("  Task id = " + str(task.id) +
                  '\t assigned to ' + str(task.assigned_machine.type.name) +
                  " " + str(task.assigned_machine.id) +
                  "\t status = " + task.status.name)

            # the next two lines format text to be added to the window and then it adds it into the "Task Statuses"
            # section.
            string = (str(task.id) + " Status: " + str(task.status.name) + "\n")
            tTaskStatus.insert(tk.END, string)
        else:
            print("  Task id = " + str(task.id) +
                  '\t assigned to ' + str(task.assigned_machine) +
                  "\t status = " + task.status.name)
window.mainloop()
