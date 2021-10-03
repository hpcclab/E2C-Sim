from BaseTask import TaskStatus
from BaseScheduler import BaseScheduler
import Config
from ReadExecutionTimes import ReadData
from array import *


class PhaseMIN1(BaseScheduler):
    machine_index = 0

    def __init__(self):
        super().__init__()

    def feed(self):
        while self.unlimited_queue:
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(None)
            self.batch_queue[empty_slot] = task

    def choose(self):
        index = 0
        task = []
        print(self.batch_queue)
        while self.batch_queue[index] is not None:
            if self.batch_queue[index] is not None:
                task.append(self.batch_queue[index])
                self.batch_queue = self.batch_queue[:index] + self.batch_queue[index + 1:] + [None]
                self.feed()
                index += 1
            else:
                print("No more task for scheduling ... \n")
                return None
        return task

    def offload(self, task):
        task.status = task.status_list['offloaded']

    def defer(self, task):
        if None in self.batch_queue:
            empty_slot = self.batch_queue.index(None)
            self.batch_queue[empty_slot] = task
        else:
            replaced_task = self.batch_queue[-1]
            self.unlimited_queue = [replaced_task] + self.unlimited_queue
            self.batch_queue[-1] = task
        task.status = TaskStatus.DEFERRED

    def drop(self, task):
        task.status = task.status_list['dropped']
        task.drop_time = Config.current_time

    def map(self, task):
        pass

    def schedule(self):
        output = []
        task = self.choose()
        for itask in task:
            quickest = Config.machines[0]
            for m in Config.machines:
                if m.available_time + itask.est_exec_time[m.getType()] < quickest.available_time + \
                        itask.est_exec_time[quickest.getType()]:
                    quickest = m
            output.insert(len(output), [quickest.id, itask])
            if self.machine_index == len(Config.machines) - 1:
                self.machine_index = 0
            else:
                self.machine_index += 1
        return output
