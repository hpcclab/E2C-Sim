import BaseMachine, datetime

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
        self._available_time += task._est_exec_time
        task.assigned_machine_id = self._id
        task._status = super().tasks_status['pending']

    def select(self):
        return self.queue[0]

    def execute(self):
        toBeRun = algorithm()
        return toBeRun

    def terminate(self, task):
        if task._status == super().tasks_status['completed']:
            self._completed.append(task._id)
            self._available_time -= task.execution_time
        else:
            self._missed.append(task._id)
            task.status = super().tasks_status['dropped']
            task.drop_time = datetime.now()
            self._available_time -= task.execution_time
        self._queue.remove(task)

    def run(self):
        while len(self._queue) != 0:
            task = self.execute()
            task._status = super().tasks_status['executing']
            task_id = task._id
            task.start_time = datetime.now()
            #code to run task on machine
            task.completion_time = datetime.now()
            task._status = super().tasks_status['completed']
            self.terminate(task)
        if len(self._queue) != 0: return 1
        else: return 0

    def shutdown(self):
        while len(self._queue) != 0:
            self.terminate(_queue[0])
        self.status = 'off'

    def info(self):
        completed = ""

        dictionary = ("ID: " + self._id + ", Type: " + self._type +
                      ", Status: " + self._status + ", Specs: " +
                      self._specs + ", Power: " + ", Estimated Available Time: " +
                      self._available_time + ", Queue: " + self._queue +
                      ", Running Task: " + "Completed Tasks: Total: " +
                      len(self._completed) + completed + ", Missed: " +
                      self._missed)
        return dictionary

    def algorithm(self):
        return self._queue[0]