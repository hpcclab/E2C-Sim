import Config
from Task import Task
from Event import Event, EventTypes
from FCFS import FCFS
from MIN import Min1
from PhaseMIN1 import PhaseMIN1
from PhaseMIN2 import PhaseMIN2
import gui
import tkinter as tk

gui1 = gui.Gui("Scheduler GUI", '1000x800', 700, 800)
gui1.create_main_queue(8)
gui1.create_machine_names()
gui1.create_legend()
gui1.create_task_stats()
gui1.create_speed_control()

# Task set up
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

            type1 = Config.find_task_types(task_type_id)
            Tasks.append(Task(task_id, type1, estimated_time,
                              execution_time, arrival_time))
for task in Tasks:
    event = Event(task.arrival_time, EventTypes.ARRIVING, task)
    Config.event_queue.add_event(event)

# Code for 2 phase scheduling
# Available Phase 1 Algorithms: PhaseMIN1()
# Available Phase 2 Algorithms: PhaseMIN2()
scheduler1 = PhaseMIN1()
scheduler2 = PhaseMIN2()

completed_count = 0
arrived_count = 0
missed_count = 0
machine_counts = []
for _ in Config.machines:
    machine_counts.append(0)

while Config.event_queue.event_list:
    print(80 * '=' + '\n\n Reading events from event queue ===>>>')
    event = Config.event_queue.get_first_event()
    Config.current_time = event.time

    if event.event_type == EventTypes.ARRIVING:
        task = event.event_details
        # function to add arrived task total
        arrived_count += 1
        gui1.arrived_total(arrived_count)
        scheduler1.unlimited_queue.append(task)

        print('Task ' + str(task.id) + ' arrived at ' + str(Config.current_time) + ' sec\n')

        scheduler1.feed()
        minList = scheduler1.schedule()
        gui1.task_queueing(task)
        assigned_machines = scheduler2.schedule(minList)
        count = 0
        while len(assigned_machines) > count:
            execute = assigned_machines.pop(count)
            execute.execute()
            count += 1

    elif event.event_type == EventTypes.COMPLETION:
        task = event.event_details
        machine = task.assigned_machine
        time = Config.current_time
        print(' Task ' + str(task.id) + ' completed at ' + str(
            Config.current_time) + ' sec on machine type ' + machine.type.name + ' machine id : ' + str(machine.id))

        # function to update the completed total
        completed_count += 1

        gui1.task_executed(task)
        gui1.completed_total(task, completed_count)
        # the next several lines update the individual machines' number of completed tasks
        machine_counts[int(machine.id) - 1] = machine_counts[int(machine.id) - 1] + 1
        stats = "Total Completed tasks on " + str(machine.type.name) + " (ID " + str(machine.id) + "): " + \
                str(machine_counts[machine.id - 1]) + "\n"

        machine.terminate()
        scheduler1.feed()
        assigned_machine = scheduler1.schedule()
        if assigned_machine:
            assigned_machine.execute()
    else:
        missed_count += 1
        gui1.missed_total(missed_count)

    print('\n' + 50 * '.')
    for task in Tasks:
        if task.assigned_machine is not None:
            print("  Task id = " + str(task.id) +
                  '\t assigned to ' + str(task.assigned_machine.type.name) +
                  " " + str(task.assigned_machine.id) +
                  "\t status = " + task.status.name)

gui1.begin()

"""
# To change scheduling method, change what scheduler variable is set to
# Available Algorithm methods: FCFS(), Min1()
scheduler = Min1()

completed_count = 0
arrived_count = 0
machine_counts = []
for _ in Config.machines:
    machine_counts.append(0)
    tStatistics.insert(tk.END, "Placeholder \n")

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
        arrived_count += 1
        tStatistics.replace(0.0, 2.0, "Total Arrived Tasks: " + str(arrived_count) + "\n")
        print(string)

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

        # the next couple lines update the total number of completed tasks
        completed_count += 1
        tStatistics.replace(2.0, 3.0, "Total Completed Tasks: " + str(completed_count) + "\n")

        # the next several lines update the individual machines' number of completed tasks
        machine_counts[int(machine.id) - 1] = machine_counts[int(machine.id) - 1] + 1
        stats = "Total Completed tasks on " + str(machine.type.name) + " (ID " + str(machine.id) + "): " + str(
            machine_counts[machine.id - 1]) + "\n"
        tStatistics.replace((3.0 + float(machine.id)), (4.0 + float(machine.id)), stats)

        machine.terminate()
        scheduler.feed()
        assigned_machine = scheduler.schedule()
        if assigned_machine:
            assigned_machine.execute()
    print('\n' + 50 * '.')
"""
