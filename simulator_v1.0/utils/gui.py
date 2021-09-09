import Config
import tkinter as tk
from PhaseMIN1 import PhaseMIN1
from PhaseMIN2 import PhaseMIN2


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

    def __init__(self, title, geometry, height, width):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry)
        self.height = height
        self.width = width
        self.canvas = tk.Canvas(self.window, bg="#fff")
        self.canvas.place(relx=0.05, rely=0.05, relwidth=.9, relheight=.9)
        self.x2 = 0
        b = tk.Button(self.window, text="Exit", command=self.window.destroy)
        b.pack(side='bottom')

    # main queue
    def create_main_queue(self, length):
        self.main = True
        self.main_queue = []
        x1, self.x2 = 50, 90

        for k in range(length):
            self.main_queue.append([k, False, None])
            self.canvas.create_rectangle(x1, self.height / 2 + 20, self.x2, self.height / 2 - 20, outline="black")
            self.coords.append(
                [x1 + 10, self.height / 2 + 10, x1 + 30, self.height / 2 + 10, x1 + 10, self.height / 2 - 5])
            x1 += 40
            self.x2 += 40
        self.coords.reverse()
        self.canvas.create_oval(x1, self.height / 2 + 20, self.x2, self.height / 2 - 20, outline="black")

    # Tasks and object legend
    def create_legend(self):
        k1, k2, y = 50, 100, 10
        for name in Config.task_types:
            self.canvas.create_text(k1, self.height / 32 + y, fill="black", font="Times 10 italic bold", text=name.name)
            self.canvas.create_polygon(k2, self.height / 32 + y - 5, k2 + 20, self.height / 32 + y + 10, k2,
                                       self.height / 32 + y + 10,
                                       outline="black", fill=self.colors[name.id])
            y += 20

    # List of machine names
    def create_machine_names(self):
        total = len(Config.machines)
        w1, z1, w2, z2 = 650, self.height / total - self.height / (
                total + 1), 720, self.height / total + 40 - self.height / (total + 1)
        for name in Config.machines:
            shrink = 0
            # creates the individual machine queues
            for k in range(name.queue_size):
                self.canvas.create_rectangle(620 - shrink, z1, 650 - shrink, z2)
                self.m_coords.append(
                    [(620 - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 + 10, (620 - shrink + 650 - shrink) / 2 + 10,
                     (z1 + z2) / 2 + 10, (620 - shrink + 650 - shrink) / 2 - 10, (z1 + z2) / 2 - 5])
                shrink += 30
            # displays the machine names
            self.canvas.create_rectangle(w1, z1, w2, z2)
            self.canvas.create_text((w1 + w2) / 2, (z1 + z2) / 2, fill="black", font="Times 10 italic bold",
                                    text=name.getType())
            shrink -= 30
            if self.main:
                self.canvas.create_line(self.x2, self.height / 2, (self.x2 + 620 - shrink) / 2, (z1 + z2) / 2,
                                        620 - shrink, (z1 + z2) / 2, smooth=1)
            z1 += self.height / total
            z2 += self.height / total

    # creates the three boxes that display the Arrived, completed and missed tasks
    def create_task_stats(self):
        self.canvas.create_rectangle(200, self.height / 32, 300, self.height / 32 + 30)
        self.canvas.create_rectangle(300, self.height / 32, 350, self.height / 32 + 30)
        self.canvas.create_text(250, self.height / 32 + 15, text="Arrived Tasks")
        self.canvas.create_text(325, self.height / 32 + 15, text=0, tags="arrived")
        self.canvas.create_rectangle(200, self.height / 32 + 30, 300, self.height / 32 + 60)
        self.canvas.create_rectangle(300, self.height / 32 + 30, 350, self.height / 32 + 60)
        self.canvas.create_text(250, self.height / 32 + 45, text="Completed Tasks")
        self.canvas.create_text(325, self.height / 32 + 45, text=0, tags="completed")
        self.canvas.create_rectangle(200, self.height / 32 + 30, 300, self.height / 32 + 90)
        self.canvas.create_rectangle(300, self.height / 32 + 30, 350, self.height / 32 + 90)
        self.canvas.create_text(250, self.height / 32 + 75, text="Missed Tasks")
        self.canvas.create_text(325, self.height / 32 + 75, text=0, tags="missed")

    def create_speed_control(self):
        b = tk.Button(self.canvas, text='Full Send', )
        b.pack(side='bottom')
        b = tk.Button(self.canvas, text='Accept Task', )
        b.pack(side='bottom')
        b = tk.Button(self.canvas, text='Execute Task', )
        b.pack(side='bottom')

    def arrived_total(self, arrived_count):
        self.canvas.delete("arrived")
        self.canvas.create_text(325, self.height / 32 + 15, text=arrived_count, tags="arrived")

    def missed_total(self, missed_count):
        self.canvas.delete("missed")
        self.canvas.create_text(325, 95, text=missed_count, tags="missed")

    def task_queueing(self, task):
        count = 0
        for spot in self.main_queue:
            if not spot[1]:
                k = spot[0]
                marker = self.canvas.create_polygon(self.coords[k][0], self.coords[k][1], self.coords[k][2],
                                                    self.coords[k][3],
                                                    self.coords[k][4], self.coords[k][5], outline="black",
                                                    fill=self.colors[task.type.id])
                spot[1] = True
                spot[2] = marker
                if spot[0] == 0:
                    self.nextIn = spot[2]
                count += 1
                break

    def task_assigned(self, task):
        m_id = task.assigned_machine.id - 1
        self.canvas.moveto(self.nextIn, self.m_coords[m_id][0], self.m_coords[m_id][5])
        self.main_queue[0][1] = False
        self.assigned_queue.append([task, self.nextIn])
        self.main_queue[0][2] = None
        k = 0
        for spot in self.main_queue:
            if spot[1] and not self.main_queue[k-1][1]:
                spot[1] = False
                self.main_queue[k - 1][1] = True
                self.canvas.move(spot[2], 40, 0)
                if self.main_queue[k-1][0] == 0:
                    self.nextIn = spot[2]
            k += 1

    def task_completed(self, task, completed_count):
        for atask in self.assigned_queue:
            if atask[0] == task:
                self.canvas.delete(atask[1])
        self.canvas.delete("completed")
        self.canvas.create_text(325, self.height / 32 + 45, text=completed_count, tags="completed")

    def begin(self):
        self.window.mainloop()


""""
lbl1.pack()
tArrivalTime.pack()
lbl2.pack()
tCompletionTime.pack()
lbl3.pack()
tTaskStatus.pack()
lbl4.pack()
tStatistics.pack()
tStatistics.insert(tk.END, "Total Arrived Tasks: 0\n")
tStatistics.insert(tk.END, "Total Completed Tasks: 0\n")
tStatistics.insert(tk.END, "Total tasks completed by each machine: \n")
tCompletionTime.insert(tk.END, "Green: under 2 seconds, Yellow: under 5 seconds, Red: over 5 seconds\n")
"""

# end of GUI window code
# the find function is used to add visualization of the status of tasks
"""
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
"""
"""
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
"""
