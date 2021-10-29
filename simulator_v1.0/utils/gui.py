import Config
from Task import Task
from Event import Event, EventTypes
import tkinter as tk
import tkinter.ttk as tk1
from PhaseMIN1 import PhaseMIN1
from PhaseMIN2 import PhaseMIN2
from PIL import ImageTk, Image


class Gui:
    main = False
    main_queue = []
    colors = [None, "green", "yellow", "red", "blue", "purple"]
    coords = []
    m_coords = []
    assigned_queue = []
    scheduler1 = PhaseMIN1()
    scheduler2 = PhaseMIN2()
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
        self.speed = tk.IntVar()
        self.speed.set(500)
        self.pb = None
        self.Tasks = []
        self.pause = 0
        self.sched = "MinMin"
        self.menu_font = ("Times New Roman", 12)
        self.menu = tk.Menu(self.window, font=self.menu_font)

    def create_controls(self):
        start_b = tk.Button(self.canvas, text="Start", command=self.start, width=5, relief="solid", font=self.menu_font, bd=1)
        stop_b = tk.Button(self.canvas, text="Pause", command=self.stop, width=5, font=self.menu_font)
        # stop_b.place(x=175, y=450)
        reset_b = tk.Button(self.canvas, text="Reset", command=self.reset, width=5, relief="solid", font=self.menu_font, bd=1)
        spdcntrl = tk.Menubutton(self.canvas, text="Speed", font=self.menu_font, relief="solid", width=6, bd=1, padx=1)
        spdcntrl.menu = tk.Menu(spdcntrl)
        spdcntrl["menu"] = spdcntrl.menu
        spdcntrl.menu.add_command(label="Default Speed", command=lambda: self.set_speed(0))
        spdcntrl.menu.add_command(label=".5x Speed", command=lambda: self.set_speed(50))
        spdcntrl.menu.add_command(label=".25x Speed", command=lambda: self.set_speed(100))
        spdcntrl.menu.add_command(label=".025x Speed", command=lambda: self.set_speed(200))
        spdcntrl.menu.add_command(label=".0025x Speed", command=lambda: self.set_speed(400))
        spdcntrl.place(x=100, y=450)
        start_b.place(x=160, y=450)
        reset_b.place(x=220, y=450)

        self.pb = tk1.Progressbar(self.canvas, orient='horizontal', length=800, mode='determinate')
        self.pb.place(x=50, y=675)

    def menubar(self):
        system = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        workload = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        report = tk.Menu(self.window, tearoff=0, font=self.menu_font)
        help_ = tk.Menu(self.window, tearoff=0, font=self.menu_font)

        self.menu.add_cascade(label='System', menu=system)
        system.add_command(label='Machines', command=None)
        system.add_command(label='Cloud', command=None)
        system.add_command(label='Energy Resource', command=None)
        system.add_separator()
        system.add_command(label='Exit', command=self.window.destroy)

        self.menu.add_cascade(label='Workload', menu=workload)
        workload.add_command(label='Task Types', command=None)
        workload.add_command(label='Upload', command=None)
        workload.add_command(label='Generate', command=None)

        self.menu.add_cascade(label='Report', menu=report)
        report.add_command(label='Tasks', command=None)
        report.add_command(label='Machines', command=None)
        report.add_command(label='Cloud', command=None)
        report.add_separator()
        report.add_command(label='Summary', command=None)

        self.menu.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Tutorial', command=None)
        help_.add_separator()
        help_.add_command(label='About', command=None)

        self.window.config(menu=self.menu)

    def set_speed(self, speed):

        self.speed_increment = speed

    def stop(self):
        self.pause = 1

    def reset(self):
        self.Tasks = []
        self.task_setup()
        self.arrived_total(0)
        self.missed_total(0)
        self.task_completed(None, 0)
        self.pb['value'] = 0
        self.pause = 0

    def task_setup(self):
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
                    self.Tasks.append(Task(task_id, type1, estimated_time,
                                           execution_time, arrival_time))
        for task in self.Tasks:
            event = Event(task.arrival_time, EventTypes.ARRIVING, task)
            Config.event_queue.add_event(event)

    def start(self):
        # speed = 0
        # speed += self.speed_increment
        self.startHelper()
        # self.window.after(speed, self.startHelper)

    def startHelper(self):
        speed = 0
        completed_count = 0
        arrived_count = 0
        missed_count = 0
        machine_counts = []
        for _ in Config.machines:
            machine_counts.append(0)
        # work on breaking here
        while Config.event_queue.event_list:
            print(80 * '=' + '\n\n Reading events from event queue ===>>>')
            event = Config.event_queue.get_first_event()
            Config.current_time = event.time
            if event.event_type == EventTypes.ARRIVING:
                task = event.event_details
                # function to add arrived task total
                arrived_count += 1
                speed += self.speed_increment
                self.window.after(speed, self.arrived_total, arrived_count)
                self.scheduler1.unlimited_queue.append(task)
                print('Task ' + str(task.id) + ' arrived at ' + str(Config.current_time) + ' sec\n')
                self.scheduler1.feed()

                self.window.after(speed, self.task_queueing, task)
                minList = self.scheduler1.schedule()
                assigned_machines = self.scheduler2.schedule(minList)
                count = 0
                while len(assigned_machines) > count:
                    execute = assigned_machines.pop(count)
                    speed += self.speed_increment
                    self.window.after(speed, self.task_assigned, execute.queue[0])
                    execute.execute()
                    count += 1
            elif event.event_type == EventTypes.COMPLETION:
                task = event.event_details
                machine = task.assigned_machine
                time = Config.current_time
                print(' Task ' + str(task.id) + ' completed at ' + str(
                    Config.current_time) + ' sec on machine type ' + machine.type.name + ' machine id : ' + str(
                    machine.id))
                # function to update the completed total
                completed_count += 1
                speed += self.speed_increment
                self.window.after(speed, self.task_completed, task, completed_count)
                # the next several lines update the individual machines' number of completed tasks
                machine_counts[int(machine.id) - 1] = machine_counts[int(machine.id) - 1] + 1
                stats = "Total Completed tasks on " + str(machine.type.name) + " (ID " + str(machine.id) + "): " + \
                        str(machine_counts[machine.id - 1]) + "\n"
                machine.terminate()
                self.scheduler1.feed()
                assigned_machine = self.scheduler1.schedule()
                if assigned_machine:
                    assigned_machine.execute()
            else:
                missed_count += 1
                speed += self.speed_increment
                self.window.after(speed, self.missed_total, missed_count)
            print('\n' + 50 * '.')
            for task in self.Tasks:
                if task.assigned_machine is not None:
                    print("  Task id = " + str(task.id) +
                          '\t assigned to ' + str(task.assigned_machine.type.name) +
                          " " + str(task.assigned_machine.id) +
                          "\t status = " + task.status.name)

    # main queue
    def create_main_queue(self, length):
        self.main = True
        self.main_queue = []
        x1, self.x2 = 50, 90
        for k in range(length):
            self.main_queue.append([k, False, None, None])
            self.canvas.create_rectangle(x1, self.height / 2 + 20, self.x2, self.height / 2 - 20, outline="black")
            self.coords.append(
                [x1 + 10, self.height / 2 + 10, x1 + 30, self.height / 2 + 10, x1 + 10, self.height / 2 - 5])
            x1 += 40
            self.x2 += 40
        self.coords.reverse()
        self.canvas.create_oval(x1, self.height / 2 + 20, self.x2 + 10, self.height / 2 - 20, outline="black")
        self.scheduler_set()

    def scheduler_set(self):
        self.canvas.delete("scheduler")
        self.canvas.create_text((self.x2 * 2 - 40) / 2 + 5, self.height / 2, text=self.sched, tags="scheduler")

    # Tasks and object legend
    def create_legend(self):
        k1, k2, y = 50, 100, 10
        for name in Config.task_types:
            self.canvas.create_text(k1, self.height / 32 + y, fill="black", font=self.menu_font, text=name.name)
            self.canvas.create_oval(k2, self.height / 32 + y - 10, k2 + 20, self.height / 32 + y + 10, outline="black",
                                    fill=self.colors[name.id])
            y += 25

    # List of machine names
    def create_machine_names(self):
        img = Image.open("cloud.png")
        img = img.resize((100, 50), Image.ANTIALIAS)
        readyimg = ImageTk.PhotoImage(img)
        label = tk.Label(self.canvas, image=readyimg)
        label.image = readyimg
        total = len(Config.machines)+1
        w1, z1, w2, z2 = 650, self.height / total - self.height / (
                total + 1), 720, self.height / total + 40 - self.height / (total + 1)
        label.place(x=620, y=z1)
        self.canvas.create_line(self.x2 + 100, z2 - 20, 620, (z1 + z2) / 2)
        self.canvas.create_line(self.x2 + 10, self.height / 2, self.x2 + 100, self.height / 2)
        self.canvas.create_line(self.x2 + 100, z1 + 20, self.x2 + 100, self.height - self.height / (total + 1) + 20)
        z1 += self.height / total
        z2 += self.height / total
        for name in Config.machines:
            shrink = 0
            # creates the individual machine queues
            start = 620
            if name.queue_size <= 3:
                for k in range(name.queue_size):
                    self.canvas.create_rectangle(start - shrink, z1, 650 - shrink, z2)
                    self.m_coords.append(
                        [(start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 + 10, (start - shrink + 650 - shrink) / 2 + 10,
                         (z1 + z2) / 2 + 10, (start - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 - 5])
                    shrink += 30
            else:
                for k in range(3):
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

            # displays the machine names
            self.canvas.create_rectangle(w1, z1, w2, z2)
            self.canvas.create_text((w1 + w2) / 2, (z1 + z2) / 2, fill="black", font="Times 12 bold",
                                    text=name.getType())
            img = Image.open(name.getType()+".png")
            img = img.resize((40, 40), Image.ANTIALIAS)
            readyimg = ImageTk.PhotoImage(img)
            label = tk.Label(self.canvas, image=readyimg)
            label.image = readyimg
            label.place(x=(w1 + w2) / 2+40, y=z1)
            shrink -= 30
            if self.main:
                self.canvas.create_line(self.x2 + 100, z2 - 20, start-shrink, (z1 + z2) / 2)
            z1 += self.height / total
            z2 += self.height / total

    # creates the three boxes that display the Arrived, completed and missed tasks
    def create_task_stats(self):
        self.canvas.create_rectangle(200, self.height / 32, 300, self.height / 32 + 30)
        self.canvas.create_rectangle(300, self.height / 32, 350, self.height / 32 + 30)
        self.canvas.create_text(250, self.height / 32 + 15, text="Total Tasks")
        self.canvas.create_text(325, self.height / 32 + 15, text=len(self.Tasks), tags="total")
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

    def arrived_total(self, arrived_count):
        self.canvas.delete("arrived")
        self.canvas.create_text(325, self.height / 32 + 45, text=arrived_count, tags="arrived")

    def missed_total(self, missed_count):
        self.canvas.delete("missed")
        self.canvas.create_text(325, 127, text=missed_count, tags="missed")

    def task_completed(self, task, completed_count):
        for atask in self.assigned_queue:
            if atask[0] == task:
                self.canvas.delete(atask[1])
                self.canvas.delete(atask[2])
        self.canvas.delete("completed")
        self.canvas.create_text(325, self.height / 32 + 75, text=completed_count, tags="completed")
        if len(self.Tasks) != 0:
            self.pb['value'] += 100 / len(self.Tasks)

    def task_queueing(self, task):
        count = 0
        for spot in self.main_queue:
            if not spot[1]:
                k = spot[0]
                marker = self.canvas.create_oval(self.coords[k][2], self.coords[k][3], self.coords[k][4],
                                                 self.coords[k][5] - 5, outline="black", fill=self.colors[task.type.id])
                text = self.canvas.create_text((self.coords[k][2] + self.coords[k][4]) / 2,
                                               (self.coords[k][4] + self.coords[k][5]) / 2 + 6, text=task.id)
                spot[1] = True
                spot[2] = marker
                spot[3] = text
                if spot[0] == 0:
                    self.nextIn = spot[2]
                    self.nextText = spot[3]
                count += 1
                break

    def task_assigned(self, task):
        m_id = task.assigned_machine.id - 1
        self.canvas.moveto(self.nextIn, self.m_coords[m_id][0], self.m_coords[m_id][5] - 5)
        self.canvas.moveto(self.nextText, (self.m_coords[m_id][0] + self.m_coords[m_id][2]) / 2 - 5,
                           self.m_coords[m_id][5])
        self.main_queue[0][1] = False
        self.assigned_queue.append([task, self.nextIn, self.nextText])
        self.main_queue[0][2] = None
        k = 0
        for spot in self.main_queue:
            if spot[1] and not self.main_queue[k - 1][1]:
                spot[1] = False
                self.main_queue[k - 1][1] = True
                if self.main_queue[k - 1][0] == 0:
                    self.nextIn = spot[2]
                    self.nextText = spot[3]
            k += 1

    def begin(self):
        self.window.mainloop()
