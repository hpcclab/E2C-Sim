"""
Authors: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021

Training a RL-based scheduler requires a training dataset. This dataset
contains a large number of arrival time files, named episodes, which are
generated based on the scenario(s). 

As an example, a training dataset of size 100 contains 100 csv files, 
ArrivalTimes-0.csv to ArrivalTimes-99.csv, where each of those files 
contains the arrival time and execution time of a certain number of tasks
generated based on a scenario(s).
"""


from os import makedirs
import tqdm

from utils.workload import Workload
import utils.config as config


class Epsiode():

    def generate(self, rate,task_hete, number_of_episodes):
        # This method is used to generate a certain number of episodes, number_of_episodes.
        # First, a scenario is selected based on the provided probabilities, then the episode
        # is generated. 
        # The output file is named in the following format:
        # workload-<rate>-<task_hete>.csv

        pbar = tqdm.tqdm(total=number_of_episodes)        
        for episode in range(number_of_episodes):
            pbar.update(1)
            folder = f"{config.path_to_workload}/workloads/workload-{rate}-{task_hete}"
            makedirs(folder, exist_ok = True)            
            workload_id = f'{rate}-{task_hete}'
            Workload(workload_id).generate(episode)
        pbar.close()
    
# Just for test
# episode = Epsiode()
# for rate in range(1,30):
#     for task_hete in range(5):    
#         print(f'Arrival Rate:{rate}  Task Heterogeneity:{task_hete}')
#         episode.generate(rate, task_hete, 30)
    

        

    



