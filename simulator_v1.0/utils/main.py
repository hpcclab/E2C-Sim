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
window.title("Scheduler GUI")
window.geometry('1920x1260')

tArrivalTime = tk.Text(window, height=10, width=75)
tCompletionTime = tk.Text(window, height=10, width=75)
tTaskStatus = tk.Text(window, height=10, width=75)
tStatistics = tk.Text(window, height=10, width=75)

lbl1 = tk.Label(window, text="Task Arrival Times")
lbl1.config(font=("Helvetica", 14))
lbl2 = tk.Label(window, text="Task Completion Times")
lbl2.config(font=("Helvetica", 14))
lbl3 = tk.Label(window, text="Current Task Statuses")
lbl3.config(font=("Helvetica", 14))
lbl4 = tk.Label(window, text="Statistics")
lbl4.config(font=("Helvetica", 14))

b = tk.Button(window, text="Exit", command=window.destroy)

lbl1.pack()
tArrivalTime.pack()
lbl2.pack()
tCompletionTime.pack()
lbl3.pack()
tTaskStatus.pack()
lbl4.pack()
tStatistics.pack()
b.pack()
tStatistics.insert(tk.END, "Total Arrived Tasks: 0\n")
tStatistics.insert(tk.END, "Total Completed Tasks: 0\n")
tStatistics.insert(tk.END, "Total tasks completed by each machine: \n")
tCompletionTime.insert(tk.END, "Green: under 2 seconds, Yellow: under 5 seconds, Red: over 5 seconds\n")


# end of GUI window code
# the find function is used to add visualization of the status of tasks
def find():
    s = ["COMPLETED", "DEFERRED", "RUNNING", "ARRIVING", "PENDING", "OFFLOADED", "DROPPED", "MISSED"]
    done = []
    for stat in s:
        idx = '0.0'
        while True:
            idx = tTaskStatus.search(stat, idx, stopindex=tk.END)
            if not idx:
                break
            done.append(idx)
            lastidx = '%s+%dc' % (idx, len(s) + 1)
            if stat == "COMPLETED" or stat == "OFFLOADED":
                tTaskStatus.tag_add('green', idx, lastidx)
                tTaskStatus.tag_config('green', foreground='green')
            elif stat == "RUNNING" or stat == "PENDING" or stat == "ARRIVING":
                tTaskStatus.tag_add('yellow', idx, lastidx)
                tTaskStatus.tag_config('yellow', foreground='yellow')
            elif stat == "DEFERRED" or stat == "DROPPED" or stat == "MISSED":
                tTaskStatus.tag_add('red', idx, lastidx)
                tTaskStatus.tag_config('red', foreground='red')
            idx = lastidx


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

# Code for 2 phase scheduling
# Available Phase 1 Algorithms: PhaseMIN1()
# Available Phase 2 Algorithms: PhaseMIN2()
scheduler1 = PhaseMIN1()
scheduler2 = PhaseMIN2()

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

        # The next few lines format text to b e added to the window and then inserts it into the "Task arriving section"
        string = ('Task ' + str(task.id) + ' arrived at ' +
                  str(Config.current_time) + ' sec\n')
        tArrivalTime.insert(tk.END, string)
        arrived_count += 1
        tStatistics.replace(0.0, 2.0, "Total Arrived Tasks: " + str(arrived_count) + "\n")
        print(string)

        scheduler1.unlimited_queue.append(task)
        scheduler1.feed()

        minList = scheduler1.schedule()
        print(minList)
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
        string = (' Task ' + str(task.id) + ' completed at ' + str(
            Config.current_time) + ' sec on machine type ' + machine.type.name + ' machine id : ' + str(machine.id))
        print(string)

        # the next five lines format text to be added to the window and then it adds it into the "Task Completion
        # Time" Section.
        if time - task.arrival_time < 2:
            tCompletionTime.insert(tk.END, 'Task ' + str(task.id) + ' completed at ')
            s = str(round(Config.current_time, 3)) + ' sec '
            tCompletionTime.insert(tk.END, s)
            idx = tCompletionTime.search(s, 1.0, tk.END)
            lastidx = '%s+%dc' % (idx, len(s))
            tCompletionTime.tag_add("good", idx, lastidx)
            tCompletionTime.tag_config("good", foreground="green")
            tCompletionTime.insert(tk.END, 'on' + ' machine type: ' + machine.type.name + ', and machine id: ' + str(
                machine.id) + "\n")
        elif time - task.arrival_time <= 5:
            tCompletionTime.insert(tk.END, 'Task ' + str(task.id) + ' completed at ')
            s = str(round(Config.current_time, 3)) + ' sec '
            tCompletionTime.insert(tk.END, s)
            idx = tCompletionTime.search(s, 1.0, tk.END)
            lastidx = '%s+%dc' % (idx, len(s))
            tCompletionTime.tag_add("okay", idx, lastidx)
            tCompletionTime.tag_config("okay", foreground="yellow")
            tCompletionTime.insert(tk.END, 'on' + ' machine type: ' + machine.type.name + ', and machine id: ' + str(
                machine.id) + "\n")
        else:
            tCompletionTime.insert(tk.END, 'Task ' + str(task.id) + ' completed at ')
            s = str(round(Config.current_time, 3)) + ' sec '
            tCompletionTime.insert(tk.END, s)
            idx = tCompletionTime.search(s, 1.0, tk.END)
            lastidx = '%s+%dc' % (idx, len(s))
            tCompletionTime.tag_add("bad", idx, lastidx)
            tCompletionTime.tag_config("bad", foreground="red")
            tCompletionTime.insert(tk.END, 'on' + ' machine type: ' + machine.type.name + ', and machine id: ' + str(
                machine.id) + "\n")

        # the next couple lines update the total number of completed tasks
        completed_count += 1
        tStatistics.replace(2.0, 3.0, "Total Completed Tasks: " + str(completed_count) + "\n")

        # the next several lines update the individual machines' number of completed tasks
        machine_counts[int(machine.id) - 1] = machine_counts[int(machine.id) - 1] + 1
        stats = "Total Completed tasks on " + str(machine.type.name) + " (ID " + str(machine.id) + "): " + \
                str(machine_counts[machine.id - 1]) + "\n"
        tStatistics.replace((3.0 + float(machine.id)), (4.0 + float(machine.id)), stats)

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
            # the next two lines format text to be added to the window and then it adds it into the "Task Statuses"
            # section.
            string = ("Task " + str(task.id) + " Status: " + str(task.status.name) + "\n")
            if tTaskStatus.get(float(task.id)) is not None:
                tTaskStatus.replace(float(task.id), tk.END, string)
            else:
                tTaskStatus.insert(tk.END, string)
        else:
            print("  Task id = " + str(task.id) +
                  '\t assigned to ' + str(task.assigned_machine) +
                  "\t status = " + task.status.name)
            string = "Task " + str(task.id) + " Status: " + str(task.status.name) + "\n"
            tTaskStatus.insert(tk.END, string)

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
# Current Task Statuses are updated here
for task in Tasks:
    if task.assigned_machine is not None:
        print("  Task id = " + str(task.type.id) +
              '\t assigned to ' + str(task.assigned_machine.type.name) +
              " " + str(task.assigned_machine.id) +
              "\t status = " + task.status.name)

        # the next two lines format text to be added to the window and then it adds it into the "Task Statuses"
        # section.
        string = ("Task " + str(task.id) + " Status: " + str(task.status.name))
        if tTaskStatus.get(float(task.id)) is not None:
            tTaskStatus.replace(float(task.id), tk.END, string + " \n")
        else:
            tTaskStatus.insert(tk.END, string)
    else:
        print("  Task id = " + str(task.type) +
              '\t assigned to ' + str(task.assigned_machine) +
              "\t status = " + task.status.name)
        string = "Task " + str(task.id) + " Status: " + str(task.status.name) + " \n"
        tTaskStatus.insert(tk.END, string)
    find()

window.mainloop()
