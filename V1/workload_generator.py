import utils.config as config
from utils.workload import Workload

scenario = 'sc-1'


for scenario in [f'sc-{k}' for k in range(1,5)]:
    seed = 100
    for i in range(30):
        seed += 7*i
        Workload().generate(scenario_name = scenario, workload_id = i, seed = seed)