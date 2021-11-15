"""
Authors: Jett Miller
Updated on: 10/31/2021

Here, a graphical interface architecture is created to provide and
interface to control and display the flow of tasks from the created workloads.

"""
import Config
import tkinter as tk
import tkinter.ttk as tk1
from PIL import ImageTk, Image


class Gui:
    main = False
    main_queue = []
    colors = [None, "green", "yellow", "red", "blue", "purple"]
    coords = []
    m_coords = []
    assigned_queue = []
    nextIn = 0
    nextText = 0

    def __init__(self, title, geometry, height, width):
        self.window = tk.Tk()          
        self.window.title(title)
        self.window.geometry(geometry)
        self.height = height
        self.width = width
        self.canvas = tk.Canvas(self.window, bg="#fff")       
        self.canvas.place(relx=0.05, rely=0.05, relwidth=.9, relheight=.9)        
        self.x2 = 0
        self.speed_increment = 0
        self.pb = None
        self.Tasks = []
        self.Task_pointer = []
        self.completeds = []
        self.pause = 0
        self.menu_font = ("Times New Roman", 10)
        self.menu = tk.Menu(self.window, font=self.menu_font)
        self.spdcntrl = tk.Menubutton(self.canvas, text="Speed", font=self.menu_font, relief="solid", width=6, bd=1, padx=1)
        self.total_tasks = 0

    def create_main_queue(self, length, sched): # creates the ready queue displayed in the middle of the gui
        self.main = True
        self.main_queue = []
        x1, self.x2 = 50, 90
        for k in range(length): # creates the correct length queue and appends the coordinates to coords.
            self.main_queue.append([k, False, None, None])
            self.canvas.create_rectangle(x1, self.height / 2 + 20, self.x2, self.height / 2 - 20, outline="black")
            self.coords.append(
                [x1 + 10, self.height / 2 + 10, x1 + 30, self.height / 2 + 10, x1 + 10, self.height / 2 - 5])
            x1 += 40
            self.x2 += 40
        self.coords.reverse() # after the coords list is created, reverse it so that the first option is first and not last.
        self.canvas.create_oval(x1, self.height / 2 + 20, self.x2 + 10, self.height / 2 - 20, outline="black") # creates the oval that contains the scheduling algorithm.
        self.scheduler_set(sched) # calls the function that sets the scheduling algorithm display

    def create_machine_names(self): # creates the list of machines available for scheduling and their queues on the right.
        # next few lines set up the image for the machines
        img = Image.open("./figures/cloud.png")
        img = img.resize((100, 50), Image.ANTIALIAS)
        readyimg = ImageTk.PhotoImage(img)
        label = tk.Label(self.canvas, image=readyimg)
        label.image = readyimg
        total = len(Config.machines)+1
        w1, z1, w2, z2 = 650, self.height / total - self.height / (
                total + 1), 720, self.height / total + 40 - self.height / (total + 1) # sets the coordinates for the
        # beginning of the machines ie the cloud at the top
        label.place(x=620, y=z1)
        # creates the lines that go from the main queue to the available machines
        self.canvas.create_line(self.x2 + 100, z2 - 20, 620, (z1 + z2) / 2)
        self.canvas.create_line(self.x2 + 10, self.height / 2, self.x2 + 100, self.height / 2)
        self.canvas.create_line(self.x2 + 100, z1 + 20, self.x2 + 100, self.height - self.height / (total + 1) + 20)
        z1 += self.height / total # increments the vertical location of the machines
        z2 += self.height / total
        for name in Config.machines: # traverses through the machines and creates their display and records their coordinates
            shrink = 0
            # creates the individual machine queues
            start = 620
            if name.queue_size <= 3: # checks if the machines' queue is less than 4, and if it is then it displays each one
                for _ in range(name.queue_size):
                    self.canvas.create_rectangle(start - shrink, z1, 650 - shrink, z2)
                    self.m_coords.append(
                        [(start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 + 10, (start - shrink + 650 - shrink) / 2 + 10,
                         (z1 + z2) / 2 + 10, (start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 - 5])
                    shrink += 30
            else: # else if the machines' queue is longer, it displays the first 4 and leaves the last one open ended
                for _ in range(3):
                    self.canvas.create_rectangle(start - shrink, z1, 650 - shrink, z2)
                    self.m_coords.append(
                        [(start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 + 10,
                         (start - shrink + 650 - shrink) / 2 + 10,
                         (z1 + z2) / 2 + 10, (start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 - 5])
                    shrink += 30
                self.canvas.create_line(start-shrink,z1, 650-shrink, z1)
                self.canvas.create_line(start-shrink,z2, 650-shrink, z2)
                self.m_coords.append(
                    [(start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 + 10,
                     (start - shrink + 650 - shrink) / 2 + 10,
                     (z1 + z2) / 2 + 10, (start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 - 5])
                shrink += 30

            # displays the machine names and their corresponding images
            self.canvas.create_text((w1 + w2) / 2 -10 , (z1 + z2) / 2 + 30, fill="black", font="Times 12 bold",
                                    text=name.getType())
            img = Image.open("./figures/"+name.getType()+".png")
            img = img.resize((50, 40), Image.ANTIALIAS)
            readyimg = ImageTk.PhotoImage(img)
            label = tk.Label(self.canvas, image=readyimg)
            label.image = readyimg
            label.place(x=w1 + 1, y=z1)
            shrink -= 30
            if self.main:
                self.canvas.create_line(self.x2 + 100, z2 - 20, start-shrink, (z1 + z2) / 2)
            z1 += self.height / total
            z2 += self.height / total

    def create_task_stats(self, total_tasks): # creates the list of all the different tasks statistics
        self.canvas.create_rectangle(200, self.height / 32, 300, self.height / 32 + 30)
        self.canvas.create_rectangle(300, self.height / 32, 350, self.height / 32 + 30)
        self.canvas.create_text(250, self.height / 32 + 15, text="Total Tasks")
        self.canvas.create_text(325, self.height / 32 + 15, text=str(total_tasks), tags="total")
        self.total_tasks = total_tasks
        self.canvas.create_rectangle(200, self.height / 32 + 30, 300, self.height / 32 + 60)
        self.canvas.create_rectangle(300, self.height / 32 + 30, 350, self.height / 32 + 60)
        self.canvas.create_text(250, self.height / 32 + 45, text="Arrived Tasks")
        self.canvas.create_text(325, self.height / 32 + 45, text=0, tags="arrived")
        self.canvas.create_rectangle(200, self.height / 32 + 60, 300, self.height / 32 + 90)
        self.canvas.create_rectangle(300, self.height / 32 + 60, 350, self.height / 32 + 90)
        self.canvas.create_text(250, self.height / 32 + 75, text="Completed Tasks")
        self.canvas.create_text(325, self.height / 32 + 75, text=0, tags="completed")
        self.canvas.create_rectangle(200, self.height / 32 + 90, 300, self.height / 32 + 120)
        self.canvas.create_rectangle(300, self.height / 32 + 90, 350, self.height / 32 + 120)
        self.canvas.create_text(250, self.height / 32 + 105, text="Missed Tasks")
        self.canvas.create_text(325, self.height / 32 + 105, text=0, tags="missed")
        self.canvas.create_rectangle(200, self.height / 32 + 120, 300, self.height / 32 + 150)
        self.canvas.create_rectangle(300, self.height / 32 + 120, 350, self.height / 32 + 150)
        self.canvas.create_text(250, self.height / 32 + 135, text="Dropped Tasks")
        self.canvas.create_text(325, self.height / 32 + 135, text=0, tags="dropped")
        self.canvas.create_rectangle(200, self.height / 32 + 150, 300, self.height / 32 + 180)
        self.canvas.create_rectangle(300, self.height / 32 + 150, 350, self.height / 32 + 180)
        self.canvas.create_text(250, self.height / 32 + 165, text="Offloaded Tasks")
        self.canvas.create_text(325, self.height / 32 + 165, text=0, tags="offloaded")

        #self.canvas.create_text(325, self.height / 32 + 165, text=self.pb['values'], tags="pb")


        self.Task_pointer = [total_tasks]

    def create_menubar(self): # Creates the menu bar located at the top of the gui
        # first four lines create the main tabs
        system = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        workload = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        report = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        help_ = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        # Next several lines create the different options associated with the first option (system) in the menu bar
        self.menu.add_cascade(label='System', menu=system)
        system.add_command(label='Machines', command=None)
        system.add_command(label='Cloud', command=None)
        system.add_command(label='Energy Resource', command=None)
        system.add_separator()
        system.add_command(label='Exit', command=self.window.destroy)
        # Next several lines create the different options associated with the second option (workload) in the menu bar
        self.menu.add_cascade(label='Workload', menu=workload)
        workload.add_command(label='Task Types', command=None)
        workload.add_command(label='Upload', command=None)
        workload.add_command(label='Generate', command=None)
        # Next several lines create the different options associated with the third option (report) in the menu bar
        self.menu.add_cascade(label='Report', menu=report)
        report.add_command(label='Tasks', command=None)
        report.add_command(label='Machines', command=None)
        report.add_command(label='Cloud', command=None)
        report.add_separator()
        report.add_command(label='Summary', command=None)
        # Next several lines create the different options associated with the fourth option (Help) in the menu bar
        self.menu.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Tutorial', command=None)
        help_.add_separator()
        help_.add_command(label='About', command=None)

        self.window.config(menu=self.menu)

    def create_legend(
            self):  # creates the legend at the top left that displays the task type and its colored shape.
        k1, k2, y = 50, 100, 10
        for name in Config.task_types:
            self.canvas.create_text(k1, self.height / 32 + y, fill="black", font=self.menu_font, text=name.name)
            self.canvas.create_oval(k2, self.height / 32 + y - 10, k2 + 20, self.height / 32 + y + 10,
                                    outline="black",
                                    fill=self.colors[name.id])
            y += 25

    def create_controls(self): # creates the controls start, stop, reset and all of the speed options
        start_b = tk.Button(self.canvas, text="Start", command=self.start, width=5, relief="solid", font=self.menu_font, bd=1)
        stop_b = tk.Button(self.canvas, text="Pause", command=self.stop, width=5, font=self.menu_font)
        reset_b = tk.Button(self.canvas, text="Reset", command=self.reset, width=5, relief="solid", font=self.menu_font, bd=1)
        self.spdcntrl.menu = tk.Menu(self.spdcntrl) # creates the dropdown box menu
        self.spdcntrl["menu"] = self.spdcntrl.menu
        self.spdcntrl.menu.add_command(label="Default Speed", command=lambda: self.set_speed(0, "Default Speed")) # creates the options in the dropdown menu
        self.spdcntrl.menu.add_command(label=".5x Speed", command=lambda: self.set_speed(50, ".5x Speed"))
        self.spdcntrl.menu.add_command(label=".25x Speed", command=lambda: self.set_speed(100, ".25x Speed"))
        self.spdcntrl.menu.add_command(label=".025x Speed", command=lambda: self.set_speed(200, ".025x Speed"))
        self.spdcntrl.menu.add_command(label=".0025x Speed", command=lambda: self.set_speed(400, ".0025x Speed"))
        # Following lines place the buttons inside of the GUI
        self.spdcntrl.place(x=100, y=450)
        start_b.place(x=160, y=450)
        reset_b.place(x=220, y=450)
        # Following lines create and places the progress bar at the bottom.
        self.pb = tk1.Progressbar(self.canvas, orient='horizontal', length=800, mode='determinate')
        self.pb.place(x=50, y=675)

    def set_speed(self, speed, text): # sets the amount of time between actions in the gui (displays)
        self.spdcntrl["text"] = text
        self.speed_increment = speed

    def stop(self): # work in progress. Function to stop the displaying of tasks
        self.pause = 1

    def reset(self): # Function to reset all of the task statistics
        self.arrived_total(0)
        self.missed_total(0)
        self.dropped_total(0)
        self.offloaded_total(0)
        self.task_completed(None, 0)
        self.pb['value'] = 0
        self.pause = 0
        self.Task_pointer = []
        self.completeds = []
        self.assigned_queue = []

    def add_task(self, num, task): # Function used to create a list of events and the corresponding task
        self.Tasks.append([num, task])

    def start(self): # Function that is execution with each click of the "start" button in the gui. displays all of the info from the list of events.
        speed = 0
        completed_count = 0
        arrived_count = 0
        missed_count = 0
        dropped_count = 0
        offloaded_count = 0
        
        for task in self.Tasks: # runs through the whole list of events
            if task[0] == 1: # If the event is an arrival, add task to the end of the queue and increment the arrived
                # total and moves task to corresponding machine queue if its been assigned.
                arrived_count += 1
                speed += self.speed_increment
                self.window.after(speed, self.arrived_total, arrived_count)
                speed += self.speed_increment
                self.window.after(speed, self.task_queueing, task[1])
                speed += self.speed_increment
                self.window.after(speed, self.task_assigned, task[1])                


            elif task[0] == 2: # If the event is missed, increment the missed total
                missed_count += 1
                speed += self.speed_increment
                self.window.after(speed, self.missed_total, missed_count)
            elif task[0] == 3: # if the event is a completion, increment the completed count and remove the task from the machine queue
                completed_count += 1
                if self.speed_increment > 0:
                    speed += self.speed_increment
                self.window.after(speed, self.task_completed, task[1], completed_count)
                self.completeds.append(task[1])
            elif task[0] == 4: # if the event is an offloaded task, increment the offloaded count
                offloaded_count += 1
                speed += self.speed_increment
                self.window.after(speed, self.offloaded_total, offloaded_count)
            elif task[0] == 5: # if the event is a dropped task, increment the dropped task and remove the task from the display
                speed += self.speed_increment
                dropped_count += 1
                self.window.after(speed, self.dropped_total, dropped_count)

    def scheduler_set(self, sched): # sets the scheduling algorithm display
        self.canvas.delete("scheduler") # deletes existing display
        self.canvas.create_text((self.x2 * 2 - 40) / 2 + 5, self.height / 2, text=sched, tags="scheduler") # replaces display

    def arrived_total(self, arrived_count): # Function to update the total arrived tasks
        self.canvas.delete("arrived")
        self.canvas.create_text(325, self.height / 32 + 45, text=arrived_count, tags="arrived")

    def missed_total(self, missed_count): # Function to update the total missed tasks
        self.canvas.delete("missed")
        self.canvas.create_text(325, 127, text=missed_count, tags="missed")

    def offloaded_total(self, offloaded_count): # Function to update the total offloaded tasks
        self.canvas.delete("offloaded")
        self.canvas.create_text(325, self.height / 32 + 165, text=offloaded_count, tags="offloaded")

    def dropped_total(self, dropped_count): # Function to update the total dropped tasks
        self.canvas.delete("dropped")
        self.canvas.create_text(325, self.height / 32 + 135, text=dropped_count, tags="dropped")

    def task_completed(self, task, completed_count): # Function to update the total completed tasks and removes the completed task from the machine queue
        if self.speed_increment > 0:
            for job in self.completeds:
                for atask in self.assigned_queue:
                    if job == atask[0] or task is not None:
                        self.canvas.delete(atask[1])
                        self.canvas.delete(atask[2])
        else:
            for atask in self.assigned_queue:
                if task == atask[0] or task is not None:
                    self.canvas.delete(atask[1])
                    self.canvas.delete(atask[2])
        self.canvas.delete("completed")
        self.canvas.create_text(325, self.height / 32 + 75, text=completed_count, tags="completed")
        if len(self.Tasks) != 0: # increments the progress bar at the bottom and ensures the total tasks aren't 0
            
            temp = 0.01 * self.pb['value'] * self.total_tasks + 1
            self.pb['value'] =  100 * temp
        
        

    def task_queueing(self, task): # adds the task to the next available spot in the queue and logs its location
        count = 0
        for spot in self.main_queue:
            if not spot[1]:
                k = spot[0]
                marker = self.canvas.create_oval(self.coords[k][2], self.coords[k][3], self.coords[k][4],
                                                 self.coords[k][5] - 5, outline="black", fill=self.colors[task.type.id])
                text = self.canvas.create_text((self.coords[k][2] + self.coords[k][4]) / 2,
                                               (self.coords[k][4] + self.coords[k][5]) / 2 + 6, text=task.id)
                self.Task_pointer.insert(task.id, [marker, text])
                spot[1] = True
                spot[2] = marker
                spot[3] = text
                if spot[0] == 0:
                    self.nextIn = spot[2]
                    self.nextText = spot[3]
                count += 1
                break

    def task_assigned(self, task): # moves the current task from the ready queue to whichever machine its been assigned
        # and shifts all of the remaining tasks in the ready queue over one space
        m_id = task.assigned_machine.id - 1
        self.canvas.moveto(self.nextIn, self.m_coords[m_id][0], self.m_coords[m_id][5] - 5)
        self.canvas.moveto(self.nextText, (self.m_coords[m_id][0] + self.m_coords[m_id][2]) / 2 - 5,
                           self.m_coords[m_id][5])
        self.main_queue[0][1] = False
        self.assigned_queue.append([task, self.nextIn, self.nextText])
        self.main_queue[0][2] = None
        k = 0
        for spot in self.main_queue: # traverses the rest of the ready queue to check if its empty and move the tasks'
            # display over if it isn't
            if spot[1] and not self.main_queue[k - 1][1]:
                spot[1] = False
                self.main_queue[k - 1][1] = True
                if self.main_queue[k - 1][0] == 0:
                    self.nextIn = spot[2]
                    self.nextText = spot[3]
            k += 1

    def begin(self): # Function called to display the window that contains the gui
        self.window.mainloop()
