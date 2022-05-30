import utils.config as config
from utils.workload import Workload
from utils.execution_time import ExecutionTime
from utils.queue import Queue
from utils.task import Task


data = config.init()
workload_id = '3-0'

for het_id in range(100):
    print(f'het:{het_id}')
    for i in range(30):        
        workload = Workload(f'het-{het_id}',f'{workload_id}')
        workload.generate(i)
        