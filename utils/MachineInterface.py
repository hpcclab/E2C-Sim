

class MachineInterface:
    def __init__(self, id, type, status, machineQueue, maxPending, workingTask):
        _ID = id
        _type = type
        _status = status
        _machineQueue = []
        _machineQueueSize = machineQueue
        _maxWorkPending = maxPending
        _workingTask = workingTask
        _stats.currentTaskStartTime
        _stats.unstartedExeTime = []
        _stats.timeSpent
        _stats.startTime

    def assignJob(self,Task):
