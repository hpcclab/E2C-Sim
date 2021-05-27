import BaseMachine

class machine(BaseMachine):

    def __init__(self, id, type, specs):
        self._id = id
        self._type = type
        self._specs = specs
        self._queue_size = Config.queue_size
        self._queue = [None] * self._queue_size
        self._status = 'off'
        self._available_time = 0.0
        self._completed = []
        self._missed = []

    def start(self):
        self.status = 'on'

    def admit(self, task):
        self._queue.append(task)
        self._available_time += task.execution_time
        task.assigned_machine_id = self._id
        task._status = super().tasks_status['offloaded']

    def select(self):
        return self.queue[0]

    def execute(self, algorithm):
        toBeRun = algorithm() #not sure how the algorithm will be used
        toBeRun._status = super().tasks_status['executing']
        return toBeRun

    def terminate(self, task):
        if task._status == super().tasks_status['completed']:
            self._completed.append(task._id)
        else:
            self._missed.append(task._id)
        self._queue.remove(task)

    def run(self):
        while self._queue != []:
            task = self.execute(algorithm)  #not sure how to choose the algorithm
            task_id = task._id
                                    #not sure what the code would be to run task on the machine
            self.terminate(task)
        if self._queue != []: return 1
        else: return 0

    def shutdown(self):
        self.status = 'off'
        while self._queue != []:
            self.terminate(_queue[0])

    def info(self):
        completed = ""

        dictionary = "ID: " + self._id + ", Type: " + self._type + ", Status: " + self._status + ", Specs: " + self._specs + ", Power: " + ", Estimated Available Time: " + self._available_time + ", Queue: " + self._queue + ", Running Task: " + "Completed Tasks: Total: " + len(self._completed) + completed + ", Missed: " + self._missed
        return dictionary
