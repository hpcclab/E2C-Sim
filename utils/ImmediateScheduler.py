from MetaScheduler import Scheduler


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
