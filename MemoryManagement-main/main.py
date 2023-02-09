"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022

"""


import utils.config as config
from utils.sol4 import Simulator
from utils.workload import Workload


config.init()
#w = Workload().generate(scenario_id = 0, workload_id = 0)
sim = Simulator()
sim.initialize(0)
sim.run()
sim.report()
sim.plot_mem_usage(['app-1','app-4','app-5'])
config.log.close()

print(sim.stats)