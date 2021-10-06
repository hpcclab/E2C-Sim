from Run import *
import tkinter as tk
import tkinter.ttk as tk1


i = 100
path_to_arrival = './Episodes/ArrivalTimes/ArrivalTimes-'+str(i)+'.txt'
run_workload = Run(scheduling_method = 'MM', path_to_arrival = path_to_arrival, id=100)






run_workload.create_event_queue()
run_workload.run()
run_workload.report('./')

