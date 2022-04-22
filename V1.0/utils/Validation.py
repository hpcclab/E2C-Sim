
"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Dec., 06 , 2021


"""
from utils.simulator import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Validation:

    
    def reset(self):
        Tasks = []
        Config.event_queue.reset()
        Config.current_time = 0.0
        Config.available_energy = Config.total_energy
        Config.cloud.reset()    
        for machine in Config.machines:
            machine.reset()


    def run(self, iteration):
        scheduling_method = 'RLS'        
        train = 0        
        low = 0
        high = 15        


        path_to_result = f'./results/validation/{iteration}'
        report_summary = open(path_to_result+'/results-summary.csv','w')
        summary_header = ['Episode', 'total_no_of_tasks','mapped', 'offloaded','cancelled','Completion%','xCompletion%','totalCompletion%','URG_missed','BE_missed','consumed_energy%']
        writer = csv.writer(report_summary)
        writer.writerow(summary_header)

        df_task_based_report = pd.DataFrame()
        count = 0 

        for i in range(low,high):
            path_to_arrival = f'./Episodes/Workloads/workload-validation/ArrivalTimes-{i}.csv'
            count += 1            
            self.reset()            
            simulation = Simulator(scheduling_method = scheduling_method, path_to_arrival = path_to_arrival, id=i, verbosity=3)  
            simulation.create_event_queue()
            simulation.set_scheduling_method()    
            simulation.scheduler.train = train
            simulation.run()
            rewards = simulation.scheduler.rewards
            rewards.to_csv(path_to_result+'/rewards-'+str(i)+'.csv')

            row, task_report = simulation.report(path_to_result+'/')   
            writer.writerows(row)
            df_task_based_report = df_task_based_report.append(task_report, ignore_index=True)    
        report_summary.close()
        df_task_based_report.to_csv(path_to_result+'/task_based_report.csv', index = False)
        


