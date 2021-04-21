from Machine import *
import Config
from ComputingTier import *


class Scheduler:
    def __init__(self):
        self._taskQueue = []
        self._machineInterfaces = []
        self._status = "off"
        self._config.maxWorkPending = 99999
        self._stats.workSubmitted = 0
        self._stats.workCompleted = 0

    def get_machine(self):
        return self._machineInterfaces

    def add_machine(self, machineInterface):
        self._machineInterfaces.append(machineInterface)
        self._config.maxWorkPending += 1

    def remove_machine(self, machineInterface):
        self._machineInterfaces.remove(machineInterface)
        self._config.maxWorkPending -= 1

    def addJob(self, Task):
        return

    def cancelJob(self, Task):
        if self._taskQueue.__contains__(Task):
            self._taskQueue.remove(Task)

    def completion(self, Task):
        return

    def scheduling(self, time):
        return

    def initialize(self):
        self._status = "On"

    def emptyQueue(self):
        self._taskQueue.clear()
