import utils.config as config
from utils.workload import Workload
import numpy as np


rates = np.round(np.concatenate(([0.001],np.linspace(0.01,0.19,19) , np.linspace(0.2,1.0,9),np.linspace(2,5,4), [10,100000]) ),3)


scenarios = []
for rate in rates:
    rate = str(rate).replace('.','_')
    scenarios.append(f'SEP_test_arrival_one_type_{rate}')



for scenario in scenarios:
    seed = 100
    for i in range(30):
        seed += 7*i
        Workload().generate(scenario_name = scenario, workload_id = i, seed = seed)