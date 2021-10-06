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
gui1.task_setup()
gui1.create_task_stats()
gui1.create_legend()
gui1.create_controls()

gui1.begin()