import utils.config as config
from utils.workload import Workload

scenarios = ['default']


for scenario in scenarios:
    seed = 100
    for i in range(1):
        seed += 7*i
        Workload().generate(scenario_name = scenario, workload_id = i, seed = seed)