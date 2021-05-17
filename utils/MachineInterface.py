

class MachineInterface:
    def __init__(self, id, type, status, machineQueue, maxPending, workingTask):
        self._ID = id
        self._type = type
        self._status = status
        self._machineQueue = []
        self._machineQueueSize = machineQueue
        self._maxWorkPending = maxPending
        self._workingTask = workingTask
        self._stats.currentTaskStartTime
        self._stats.unstartedExeTime = []
        self._stats.timeSpent
        self._stats.startTime

    def assignJob(self, Task):
        self._machineQueue.add(Task)
        self._stats.unstartedExeTime.add(Task.execution_time)

    def pendingEstimation(self, currentTime):
        return self._workingTask.EstimateExeTime - (currentTime-self._stats.currentTaskStartTime) + self._stats.unstartedExeTime

    def getQueueLen(self):
        return len(self._machineQueue)

