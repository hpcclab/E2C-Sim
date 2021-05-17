from MetaScheduler import Scheduler
import time_estimator


class ISchedulerRR:
    _previouslyAssign = 0
    metaScheduler = Scheduler()
    machines = []

    def initialize(self):
        self.metaScheduler.initialize()
        self._previouslyAssign = 0
        self.machines = self.metaScheduler.get_machine()

    def addJob(self, Task):
        if self._previouslyAssign > len(self.machines):
            self._previouslyAssign = 0
        self.machines[self._previouslyAssign].assignJob(Task)
        self._previouslyAssign += 1


class ISchedulerMAT:
    metaScheduler = Scheduler()
    machines = []

    def initialize(self):
        self.metaScheduler.initialize()
        self.machines = self.metaScheduler.get_machine()

    def addJob(self, task):
        shortest = self.machines[0]
        i = len(self.machines)
        j = 0
        while j < i:
            if self.machines[j].getQueueLen() < shortest.getQueueLen():
                shortest = self.machines[j]
            j += 1
        shortest.assignJob(task)


class ISchedulerMET:
    metaScheduler = Scheduler()
    machines = []

    def initialize(self):
        self.metaScheduler.initialize()
        self.machines = self.metaScheduler.get_machine()

    def addJob(self, task):
        estimator = time_estimator
        shortest = self.machines[0]
        i = len(self.machines)
        j = 0
        while j < i:
            if estimator.estimate(self.machines[j], task.task_type_id) < estimator.estimate(self.shortest,
                                                                                            task.task_type_id):
                shortest = self.machines[j]
            else:
                if estimator.estimate(self.machines[j], task.task_type_id) == estimator.estimate(self.shortest,
                                                                                                 task.task_type_id):
                    if self.machines[j].getQueueLen() < shortest.getQueueLen():
                        shortest = self.machines[j]
            j += 1
        shortest.assignJob(task)


class ISchedulerMCT:
    metaScheduler = Scheduler()
    machines = []

    def initialize(self):
        self.metaScheduler.initialize()
        self.machines = self.metaScheduler.get_machine()

    def addJob(self, task):
        estimator = time_estimator
        shortest = self.machines[0]
        expected = []
        incoming = 0
        for t in self.machines:
            for tasks in self.machines[t].getQueueLen():
                incoming += estimator.estimate(self.machines[t], tasks)
            expected.append(incoming)
            incoming = 0
        expectedSorted = expected
        expectedSorted.sort()
        for i in expected:
            if expectedSorted[0] == expected[i]:
                shortest = self.machines[i]
        shortest.assignJob(task)
