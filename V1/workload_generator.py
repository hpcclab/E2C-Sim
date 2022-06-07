import utils.config as config
from workload.generator import workloads_generator




workload_name = 'heterogeneous'
scenario_subname = '3'
config.init()



workloads_generator(workload_name, scenario_subname, is_etc_exist=False, is_et_exist=False)