from BaseTask import TaskStatus
from BaseScheduler import BaseScheduler
import Config
from ReadExecutionTimes import ReadData


class PhaseMIN2(BaseScheduler):
    machine_index = 0

    def __init__(self):
        super().__init__()

    def feed(self):
        while self.unlimited_queue and (None in self.batch_queue):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(None)
            self.batch_queue[empty_slot] = task

    def choose(self):
        index = 0
        print(self.batch_queue)
        if self.batch_queue[index] is not None:
            task = self.batch_queue[index]
            self.batch_queue = self.batch_queue[:index] + self.batch_queue[index + 1:] + [None]
            self.feed()
            return task
        else:
            print("No more task for scheduling ... \n")
            return None

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

    def map(self, task, machine):
        assignment = machine.admit(task)

        if assignment:
            task.assigned_machine = machine
            print('Task ' + str(task.id) + " assigned to " +
                  machine.type.name + " " + str(machine.id))
        else:
            self.defer(task)
            print("Task " + str(task.id) + " is deferred")

    def schedule(self, minlist):
        reader = ReadData()
        toMap = []
        machines1 = []
        # builds a list containing lists with each first index as a machine id and the second as the machine type
        # it also builds a list of the machines
        for m in Config.machines:
            toMap.append([m.id, m.getType()])
            machines1.append(m)
        # adds all of the tasks assigned to the list with its corresponding machine id
        if minlist is not None:
            for taskpairs in minlist:
                for machines in toMap:
                    if taskpairs[0] == machines[0]:
                        machines.append(taskpairs.pop(1))

        # finds the task assigned to each machine with the quickest execution time and maps it
        readyMachines = []
        for machine in toMap:
            if len(machine) > 2:
                quickest = machine[2]
                for task in machine:
                    if task != machine[0] and task != machine[1]:
                        print(reader.read_execution_time(task.type.id, machine[1]))
                        if task.est_exec_time[machine[1]] < quickest.est_exec_time[machine[1]]:
                            quickest = task
                            minlist.append([machine[0], quickest])
                        else:
                            minlist.append([machine[0], quickest])
                self.map(quickest, machines1[machine[0] - 1])
                readyMachines.append(machines1[machine[0]-1])
                machine.remove(quickest)
            else:
                pass

        for machine in toMap:
            for task in machine:
                if task != machine[0] and task != machine[1]:
                    self.batch_queue.append(task)
        return readyMachines

"""
            for i in minlist:
                quickest = minlist[i][0]
                for j in minlist[i]:
                    if minlist[i][j].est_exec_time < quickest.est_exec_time:
                        quickest = minlist[i][j]
                self.map(quickest, Config.machines[i])
                minlist.remove(minlist[i][j])
        else:
            print("No more tasks for scheduling in set... \n")
        for k in minlist:
            for l in minlist[k]:
                self.batch_queue.append(minlist[k][l])
            """
