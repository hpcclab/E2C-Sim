import Config
import tkinter as tk


class Gui:
    main = False

    def __init__(self, title, geometry, height, width):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry)
        self.height = height
        self.width = width
        self.canvas = tk.Canvas(
            self.window,
            height=height,
            width=width,
            bg="#fff"
        )
        self.x2 = 0
        b = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.canvas.pack()
        b.pack()

    # main queue
    def create_main_queue(self):
        self.main = True
        x1, y1, self.x2 = 50, 300, 90
        for k in range(8):
            self.canvas.create_rectangle(x1, self.height / 2 + 20, self.x2, self.height / 2 - 20, outline="black")
            x1 += 40
            self.x2 += 40
        self.canvas.create_oval(x1, self.height / 2 + 20, self.x2, self.height / 2 - 20, outline="black")

    # Tasks and object legend
    def create_legend(self):
        k1, k2, y = 50, 100, 10
        colors = [None, "green", "yellow", "red", "blue"]
        for name in Config.task_types:
            self.canvas.create_text(k1, self.height / 32 + y, fill="black", font="Times 10 italic bold", text=name.name)
            self.canvas.create_polygon(k2, self.height / 32 + y - 5, k2 + 15, self.height / 32 + y + 10, k2,
                                       self.height / 32 + y + 10,
                                       outline="black", fill=colors[name.id])
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

    def arrived_total(self, arrived_count):
        self.canvas.delete("arrived")
        self.canvas.create_text(325, self.height / 32 + 15, text=arrived_count, tags="arrived")

    def completed_total(self, completed_count):
        self.canvas.delete("completed")
        self.canvas.create_text(325, self.height / 32 + 45, text=completed_count, tags="completed")

    def missed_total(self, missed_count):
        self.canvas.delete("missed")
        self.canvas.create_text(325, 95, text=missed_count, tags="missed")

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
