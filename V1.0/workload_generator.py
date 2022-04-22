import utils.config as config
from utils.workload import Workload
from utils.execution_time import ExecutionTime
from utils.queue import Queue
from utils.task import Task


data = config.init()


for rate in range(9,10):
    for task_hete in range(0,1):
        for i in range(30):
            workload = Workload(0,0,f'{rate}-{task_hete}')
            workload.generate(i)
            #et = ExecutionTime().sample(1,'cpu',100)
            
# data = config.init()
# H = 2
# a = 0

# for rate in range(3,4):
#     for task_hete in range(2,3):
#         for i in range(30):
#             workload = Workload(H,a,f'H-{rate}-{task_hete}')
#             workload.generate(i)
#             #et = ExecutionTime().sample(1,'cpu',100)

# for i in range(30):
#     workload = Workload('toy-2')
#     workload.generate(i)
    
