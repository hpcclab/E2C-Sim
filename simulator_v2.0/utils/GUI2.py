from tkinter import * 
from tkinter.ttk import * 

from time import strftime


class GUI:




    def __init__(self):
        self.root= Tk()
        self.root.geometry('1000x800')
        self.root.title('E2C Simulator')
        self.menu_font = ("San Francisco", 14)
        self.menu = Menu(self.root, font = self.menu_font)
        


    def menubar(self):
        system = Menu(self.menu, tearoff = 0, font = self.menu_font)
        workload = Menu(self.menu, tearoff = 0, font = self.menu_font)
        report = Menu(self.menu, tearoff = 0, font = self.menu_font)
        help_ = Menu(self.menu, tearoff = 0, font = self.menu_font)

        self.menu.add_cascade(label='System', menu = system)
        system.add_command(label='Machines', command=None)
        system.add_command(label='Cloud', command=None)
        system.add_command(label='Energy Resource', command=None)
        system.add_separator()
        system.add_command(label = 'Exit', command = self.root.destroy)


        self.menu.add_cascade(label='Workload', menu = workload)
        workload.add_command(label='Task Types', command=None)
        workload.add_command(label='Upload', command = None)
        workload.add_command(label='Generate', command=None)


        self.menu.add_cascade(label='Report', menu = report)
        report.add_command(label='Tasks', command = None)
        report.add_command(label='Machines', command = None)
        report.add_command(label='Cloud', command = None)
        report.add_separator()
        report.add_command(label='Summary', command = None)



        self.menu.add_cascade(label='Help', menu = help_)
        help_.add_command(label='Tutorial', command = None)
        help_.add_separator()
        help_.add_command(label='About', command = None)



        self.root.config(menu = self.menu)
        
    def begin(self):
        
        self.root.mainloop()


gui = GUI()

gui.menubar()
gui.begin()



