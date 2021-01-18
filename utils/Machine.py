"""
Authors: Ali Mokhtari, Chavit Denninart
Created on Jan. 07, 2021.

Machine class is used to create machines while each has a "machine_id"
and "machine_type". 
"start"/"shutdown" a machine are methods defined here to start using a
machine or shut it down.
A task is added to the machine queue, then start executing the task, and
finally completed using "add_task", "start_task", and "completing_task" 
methods.

"""

from Task import *
from EventQueue import *
from  Simulator import *
import Config
#from ReadExecutionTimes import * 

class Machine:
    # Machine class is used to imitate machines in the system. Each
    # machine instance is created using "machine_id" and "machine_type".
    # A Simulator and EventQueue instances are also needed. These
    # instances are shared among all Machine instances. 
    # simulator is used to get current time.
    # event_queue.event_list is used to get "arriving"/"completion" and
    # insert completion events to event_list of event_queue.
    # A machine is initialized with "shutdown" status.
    
    # machine_id: an integer assigned to the machine which is specific to
    # each machine.
    # machine_type: string explains the type of machine. It can be "CPU",
    # "GPU", or "FPGA".
    # status: It shows the machine status that can be "shutdown", "running",
    # or "idle". "shutdown" status means that the machine cannot accept any
    # task added to its pending queue. "idle" meanse that there is no task
    # neither in the pending_queue or currently be executed in the machine.
    # queue_length: An integer that indicates the length of machine queue
    # pending_queue: the machine queue
    # completion_queue: a queue that completed task append to it
    # expected_available_time: the expected or estimation of completion time
    # last task in pending_queue.
    # running_task: It is a single element list contain the task currently
    # running in the machine. 
    
    
    simulator = Simulator()
    event_queue = EventQueue()
    
    def __init__(self, machine_id, machine_type):
        self.machine_id = machine_id
        self.machine_type = machine_type
        self.status = 'shutdown'
        self.queue_length = Config.queue_length
        self.pending_queue = []
        self.completion_queue = []
        self.expected_available_time = 0.0 
        self.running_task=[];
        
    
    def start(self):
        # start the machine. By starting a machine, it means that the 
        # machine can accept task.
        
        # assert that the machine is not currently running or idle. 
        assert self.status == 'shutdown', "Machine "+ \
            str(self.machine_id)+ " is currently "+str(self.status)
        # the status changed to idle   
        self.status = 'idle'
    
    
    def add_task(self, task):
        # It take a task and adds it to the pending_queue.
        # By adding a task to the pending_queue, its status changed to
        # "pending". 
        # The expected_available_time is also incremented by task
        # estimation of its execution time on this machine.
        # Finally, running_queue() is called to check if there is not
        # running_task, then the machine start executing current task.
        
        assert(self.status == 'running' or self.status == 'idle'), \
            "Task "+ str(task.task_id)+" cannot be assigned to the machine " \
                +str(self.machine_id) + " that is currently " + self.status
                
        task.status = 'pending'       
        self.pending_queue.append(task)
        self.expected_available_time += task.estimated_time[self.machine_type]
        self.running_queue()
    
    def start_task(self, task):
        # It takes a task and start executing the task on the machine.
        # So, the status of task changed to "executing".
        # A completion_time of the task is calculated based on the real
        # execution time and a "completion" event is added to event_queue.
        
        task.status ='executing'
        self.running_task.append(task)        
        task.completion_time = self.simulator.get_current_time() + \
            task.execution_time[self.machine_type]
        event = Event(task.completion_time, 'completion',
                      task)
        self.event_queue.add_event(event)
    
    
    def completing_task(self):
        # A completing_task is called whenever a "completion" event occurs.
        # It changed the status of "executing" task to "completed" and set
        # the completion time of the task. 
        # the task is also added to the completion_queue of the machine.
        
        task = self.running_task[0]        
        assert(self.status == 'running' or self.status == 'idle'), \
            "Task "+ str(task.task_id)+" cannot be assigned to the machine " \
                +str(self.machine_id) + " that is currently " + self.status 
        # the current time is set as completion time of the task.        
        task.completion_time = self.simulator.get_current_time() 
        task.status = 'completed'
        self.completion_queue.append(task)
        self.running_task=[]
        self.running_queue()        
        
    
    def running_queue(self):
        # It checks if the running_task is empty and there is a task in 
        # pending_queue, the task in head of pending_queue is popped and
        # is executed by the machine. 
        # If the machine is currently busy, the tasks in the pending_queue
        # should wait until completion the running_task.
        
        if(self.pending_queue and (not self.running_task)):
           self.start_task(self.pending_queue.pop(0))
           
       
    
    def shutdown(self, shutdown_type='normal'):
        # "normal" shutdown changes the status of the machine to "shutdown"
        # but continue executing tasks have already assigned to the machine(
        # tasks in pending_queue or running_task)
        # "force" shutdown not only change the status of the machine to
        # "shutdown" but also drops all task in pending_queue or 
        # running_task.
        
        assert (self.status == 'running' or self.status == 'idle'), \
            "Warning: Machine "+str(self.machine_id)+ " is currently "+ \
                str(self.status)
                
        if shutdown_type == 'force':
            
            if not self.running_task:
                task = self.running_task[0]
                print("Warning: There is an attempt to shutdowm " +
                      str(self.machine_id)+ " while task "+
                      str(task.task_id)+" is currently running" +
                      " on this machine.\n ")
                
                task.status = 'dropped'
                task.drop_time = self.simulator.get_current_time()
                self.running_task = []
        
            if not self.pending_queue:
                for task in self.pending_queue:
                    task.status = 'dropped'
                    task.drop_time = self.simulator.get_current_time()
                    self.pending_queue.remove(task)
                    
        self.status = 'shutdown'
    
    def query_info(self):
        pass