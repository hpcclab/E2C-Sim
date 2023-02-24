from  os import listdir
from workload.workload import Workload
from workload.execution_time import ExecutionTime
from workload.etc_matrix import ETC
import utils.config as config




def workloads_generator(workload_name,scenario_subname , is_etc_exist = True, is_et_exist = True,
 no_of_etcs = 100, et_set = [100,10,10,100,10,100,100,1,1]  ,et_variance=0.05, et_size=1000, sample_size = 30):
    
    if not is_etc_exist:        
        etc = ETC(workload_name)
        etc.generate(config.task_type_names, config.machine_type_names, et_set, no_of_etcs, seed =100)
        etc.hindices()

    path_to_etcs = f"./workload/etcs/{workload_name}"
    etc_files = listdir(path_to_etcs) 
    if   'hindices.csv' in etc_files:
        etc_files.remove('hindices.csv') 
    

    if not is_et_exist:
        for etc_file in etc_files:
            print(f'Execution Time for {etc_file} is generated ...')
            et = ExecutionTime(workload_name)
            etc_id = etc_file.split('.')[0]
            for task_type in config.task_type_names:
                for machine_type in config.machine_type_names:
                    et.synthesize(etc_id, task_type, machine_type, et_variance, et_size)

    workload = Workload(workload_name)
    for etc_file in etc_files:
        etc_id = etc_file.split('.')[0]    
        seed = 11
        print(f'ETC: {etc_id}')
        for i in range(sample_size):
            seed = seed + 7*i
            workload.reset()        
            workload.generate(scenario_subname=scenario_subname,
                            etc_name = etc_id,
                            workload_id = i,
                            seed=seed )

