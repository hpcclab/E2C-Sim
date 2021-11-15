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

from WorkloadGenerator import *
from os import listdir
from os.path import isfile, join
import tqdm


class Epsiode():

    
    def __init__(self, path_to_scenarios, path_to_output, scenarios_probs):
        # The scenraios that are used to generate episodes are stored in 
        # path_to_scenarios. 
        # Each scenario could be selected based on the probabilities given 
        # in scenarios_probs.
        # For example, if scenarios-0.txt to scerianos-4.txt with scenarios_probs
        # [0.1, 0.2, 0.1, 0.3, 0.3] are defined to generate 100 episodes, scenarios-1.txt 
        # with probability 20% will be used in that process. 

        self.path_to_scenarios = path_to_scenarios
        self.path_to_output = path_to_output
        self.scenarios_probs = scenarios_probs
        self.scenarios_files = [f for f in listdir(path_to_scenarios) if isfile(join(path_to_scenarios, f))]
        self.scenarios_files.sort()



    def generate_episodes(self, number_of_episodes):
        # This method is used to generate a certain number of episodes, number_of_episodes.
        # First, a scenario is selected based on the provided probabilities, then the episode
        # is generated. 
        # The output file is named in the following format:
        # ArrivalTimes-<episode_number>.csv

        pbar = tqdm(total=number_of_episodes)

        if sum(self.scenarios_probs) != 1:
            print('ERROR: The sum of scenario probabilities must be 1.')
            return 0

        count_scenarios = np.zeros(len(self.scenarios_files))
        for episode in range(number_of_episodes):
            pbar.update(1)            
            path_to_output = self.path_to_output + 'ArrivalTimes-'+str(episode)+'.csv'
                       
            cumalative_prob = [sum(self.scenarios_probs[:x]) for x in range(1,len(self.scenarios_probs)+1)]
            # a random number is generated, then based on its value and cumulative probabilits a scenario
            # is selected.
            p = random.random()
            scenario_index = next(x for x, val in enumerate(cumalative_prob)
                                        if val > p)
            count_scenarios[scenario_index]+=1
            path_to_scenario = self.path_to_scenarios + 'Scenario-' + str(scenario_index) +'.txt'            

            work_load = Workload(path_to_scenarios = path_to_scenario,
                                            path_to_output= path_to_output)
            aggregated_arrival_times = work_load.generate()
            work_load.write_to_file(aggregated_arrival_times)

        return count_scenarios
    
def test_episode_generator():
    count_scenarios = Epsiode(path_to_scenarios = './Episodes/Scenarios/',
     path_to_output = './Episodes/oversubscription-2/medium-variance/',
     scenarios_probs = [1.0]).generate_episodes(530)

    return count_scenarios

# Just for test
test_episode_generator()

        

    



