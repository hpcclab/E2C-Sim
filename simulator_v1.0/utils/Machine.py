from BaseMachine import BaseMachine, MachineStatus
from BaseTask import TaskStatus
from Event import Event, EventTypes
import Config


class Machine(BaseMachine):

    def __init__(self, id, type, specs):
        self.id = id
        self.type = type
        self.specs = specs
        self.queue_size = Config.queue_size
        self.queue = [None] * Config.queue_size
        self.status = MachineStatus.IDLE
        self.available_time = 0.0
        self.completed_tasks = []
        self.running_task = []
        self.missed = []
        self.stats = {'assigned_tasks': 0,
                      'completed_tasks': 0,
                      'missed_tasks': 0,
                      'energy_usage': 0}

    def start(self):
        self.status = MachineStatus.IDLE

    def admit(self, task):
        if None in self.queue:
            empty_slot = self.queue.index(None)
            self.queue[empty_slot] = task
            task.status = TaskStatus.PENDING
            self.available_time += task.est_exec_time[self.type.name]
            self.stats['assigned_tasks'] += 1
            print("Task " + task.type.name + " successfully assigned to " +
                  "machine " + self.type.name + " " + str(self.id))
            return 1
        else:
            print("Warning: Task " + str(task.id) + " mapped to machine " +
                  str(self.id) + " that has no empty slot\n")
            return 0

    def select(self):
        if self.queue[0] is not None:
            index = 0
            return index
        else:
            print('Warning: No more task for running on machine ' + str(self.id))
            self.status = MachineStatus.IDLE
            return None

    def execute(self):
        index = self.select()
        if index is not None and not self.running_task:
            task = self.queue[index]
            task.status = TaskStatus.RUNNING
            self.running_task.append(task)
            self.queue = self.queue[:index] + self.queue[index + 1:] + [None]
            task.completion_time = Config.current_time + task.execution_time[self.type.name]
            event = Event(task.completion_time, EventTypes.COMPLETION, task)
            Config.event_queue.add_event(event)

    def terminate(self):
        task = self.running_task.pop()
        if task.completion_time <= task.deadline:
            task.status = TaskStatus.COMPLETED
            self.completed_tasks.append(task)
            self.stats['completed_tasks'] += 1

        else:
            self.missed.append(task)
            task.status = TaskStatus.MISSED
            task.drop_time = Config.current_time

        self.available_time -= task.est_exec_time[self.type.name]
        self.execute()

    def shutdown(self):

        self.status = MachineStatus.OFF

    def info(self):
        # Incomplete as of now
        completed = ""

        dictionary = ("ID: " + self.id + ", Type: " + self.type +
                      ", Status: " + self.status)
        print(dictionary)
        return dictionary
