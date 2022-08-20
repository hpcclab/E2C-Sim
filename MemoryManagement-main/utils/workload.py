"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022

"""
import pandas as pd
import os
import sys


from utils.random_sample import RandomSample
import utils.config as config



class Workload:

    def __init__(self):
        self.path_to_workloads = './workloads'
        self.path_to_scenario = './scenarios'
        self.request_times = pd.DataFrame(columns = ['app','request_time'])        
        os.makedirs(self.path_to_workloads, exist_ok = True)


    def generate(self,workload_id, scenario_id):
        path_to_scenario = f'{self.path_to_scenario}/scenario-{scenario_id}.csv'              
        try:
            assert (os.path.isfile(path_to_scenario)), f'ERROR[workload.py -> generate()]: The path to scenario does not exist: {path_to_scenario}'
        except AssertionError as err:
            print(err)
            sys.exit()
       
        self.sc = pd.read_csv(path_to_scenario)                     
        rndSample = RandomSample()
        for _ , row in self.sc.iterrows():            
            app_name = row[0]            
            try:                
                assert (app_name in config.apps_names), f'ERROR[workload.py -> generate()]: The {app_name} is not listed in Config.json'
            except  AssertionError as err:
                print(err)
                sys.exit()
            start = row[1] + config.window       
            end = row[2]
            dist = row[3]
            no_of_requests = row[4]            
            request_times =  rndSample.generate(dist, start, end, no_of_requests)
            df = pd.DataFrame(data = request_times, columns=['request_time'])             
            df.insert(1,'app',app_name)              
            self.request_times = self.request_times.append(df,ignore_index=True)
        self.request_times = self.request_times.sort_values(by = ['request_time'])
        self.request_times = self.request_times.reset_index(drop=True)                
        self.request_times.to_csv(f'{self.path_to_workloads}/workload-{workload_id}.csv', index = False)

        return self.request_times
    

    def read_workload(self, workload_id):
        path_to_workload = f'{self.path_to_workloads}/workload-{workload_id}.csv'
        self.request_times = pd.read_csv(path_to_workload)

        return self.request_times

def test():
    workload = Workload()    
    workload.generate(scenario_id = 0, workload_id = 0)
    print(workload.request_times.head())
    
    return workload.request_times
    
   
if __name__ == '__main__':    
    workload = test()


