# =============================================================================
# 
# # Code for 2 phase scheduling: Work in progress
# # Available Algorithms: PhaseMIN1(), PhaseMIN2()
# scheduler1 = PhaseMIN1()
# scheduler2 = PhaseMIN2()
# 
# while Config.event_queue.event_list:
# 
#     print(80 * '=' + '\n\n Reading events from event queue ===>>>')
#     event = Config.event_queue.get_first_event()
#     Config.current_time = event.time
# 
#     if event.event_type == EventTypes.ARRIVING:
#         task = event.event_details
#         string = ('Task ' + str(task.id) + ' arrived at ' +
#                   str(Config.current_time) + ' sec\n')
#         tArrivalTime.insert(tk.END, string)
#         print(string)
# 
#         scheduler1.unlimited_queue.append(task)
#         scheduler1.feed()
#         minList = scheduler1.schedule()
#         print(minList)
#         assigned_machine = scheduler2.schedule(minList)
#         if assigned_machine:
#             assigned_machine.execute()
# 
#     elif event.event_type == EventTypes.COMPLETION:
# 
#         task = event.event_details
#         machine = task.assigned_machine
#         string = ('\n\t Task ' + str(task.id) + ' completed at ' +
#                   str(Config.current_time) + ' sec on :' +
#                   '\n\t\t machine type: ' + machine.type.name +
#                   '\n\t\t machine id : ' + str(machine.id))
#         print(string)
# 
#         # the next five lines format text to be added to the window and then it adds it into the "Task Completion
#         # Time" Section.
#         string = ('Task ' + str(task.id) + ' completed at ' +
#                   str(round(Config.current_time, 3)) + ' sec on' +
#                   ' machine type: ' + machine.type.name +
#                   ', and machine id: ' + str(machine.id) + "\n")
#         tCompletionTime.insert(tk.END, string)
# 
#         machine.terminate()
#         scheduler1.feed()
#         assigned_machine = scheduler1.schedule()
#         if assigned_machine:
#             assigned_machine.execute()
# 
#     print('\n' + 50 * '.')
# 
#     for task in Tasks:
#         if task.assigned_machine is not None:
#             print("  Task id = " + str(task.id) +
#                   '\t assigned to ' + str(task.assigned_machine.type.name) +
#                   " " + str(task.assigned_machine.id) +
#                   "\t status = " + task.status.name)
#             # the next two lines format text to be added to the window and then it adds it into the "Task Statuses"
#             # section.
#             string = ("Task " + str(task.id) + " Status: " + str(task.status.name))
#             if tTaskStatus.get(float(task.id)) is not None:
#                 tTaskStatus.replace(float(task.id), tk.END, string + " \n")
#             else:
#                 tTaskStatus.insert(tk.END, string)
#         else:
#             print("  Task id = " + str(task.id) +
#                   '\t assigned to ' + str(task.assigned_machine) +
#                   "\t status = " + task.status.name)
#             string = "Task " + str(task.id) + " Status: " + str(task.status.name) + " \n"
#             tTaskStatus.insert(tk.END, string)
# =============================================================================

# To change scheduling method, change what scheduler variable is set to
# Available Algorithm methods: FCFS(), Min1()
# scheduler = FCFS()
# while Config.event_queue.event_list:

#     print(60 * '+' + '\n\n--Reading events from event queue ===>>>')
#     event = Config.event_queue.get_first_event()    
#     Config.current_time = event.time

#     if event.event_type == EventTypes.ARRIVING:
#         task = event.event_details

#         # the next three lines format text to be added to the window and then it adds it into the "Task Arrival Times"
#         # Section.
#         string = ('--Task ' + str(task.id) + ' arrived at ' +
#                   str(Config.current_time) + ' sec\n')
#         # tArrivalTime.insert(tk.END, string)
#         print(string)
#         scheduler.unlimited_queue.append(task)
#         scheduler.feed()
#         assigned_machine = scheduler.schedule()
#         # if assigned_machine:
#         #     assigned_machine.execute()

#     elif event.event_type == EventTypes.COMPLETION:

#         task = event.event_details
#         machine = task.assigned_machine
#         string = ('\n---Task ' + str(task.id) + ' completed at ' +
#                   str(Config.current_time) + ' sec on :' +
#                   '\n\t\t machine type: ' + machine.type.name +
#                   '\n\t\t machine id : ' + str(machine.id))
#         print(string)

#         # the next five lines format text to be added to the window and then it adds it into the "Task Completion
#         # Time" Section.
#         string = ('Task ' + str(task.id) + ' completed at ' +
#                   str(round(Config.current_time, 3)) + ' sec on' +
#                   ' machine type: ' + machine.type.name +
#                   ', and machine id: ' + str(machine.id) + "\n")
#         # tCompletionTime.insert(tk.END, string)

#         machine.terminate()
#         scheduler.feed()
#         assigned_machine = scheduler.schedule()
#         # if assigned_machine:
#         #     assigned_machine.execute()

#     print('\n' + 60 * '+')

#     for task in Tasks:
#         if task.assigned_machine is not None:
#             print("  Task id = " + str(task.id) +
#                   '\t assigned to ' + str(task.assigned_machine.type.name) +
#                   " " + str(task.assigned_machine.id) +
#                   "\t status = " + task.status.name)

#             # the next two lines format text to be added to the window and then it adds it into the "Task Statuses"
#             # section.
#             string = ("Task " + str(task.id) + " Status: " + str(task.status.name))
#             # if tTaskStatus.get(float(task.id)) is not None:
#             #     tTaskStatus.replace(float(task.id), tk.END,  string + " \n")
#             # else:
#             #     tTaskStatus.insert(tk.END, string)

#         else:
#             print("  Task id = " + str(task.id) +
#                   '\t assigned to ' + str(task.assigned_machine) +
#                   "\t status = " + task.status.name)
#             string = "Task " + str(task.id) + " Status: " + str(task.status.name) + " \n"
#             # tTaskStatus.insert(tk.END, string)

# window.mainloop()