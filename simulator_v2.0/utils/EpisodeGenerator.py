from WorkloadGenerator import *
from os import listdir
from os.path import isfile, join


class Epsiode():

    
    def __init__(self, path_to_scenarios, path_to_output, scenarios_probs):
        self.path_to_scenarios = path_to_scenarios
        self.path_to_output = path_to_output
        self.scenarios_probs = scenarios_probs
        self.scenarios_files = [f for f in listdir(path_to_scenarios) if isfile(join(path_to_scenarios, f))]
        self.scenarios_files.sort()



    def generate_episodes(self, number_of_episodes):
        print('\n===== EPISODE GENERATING ==>>>>>>>>>>>>>')
        print('Number of episodes: '+ str(number_of_episodes))
        print('Scenarios: ' , self.scenarios_files)
        print('The probability of choosing each scenario: ', self.scenarios_probs)
        if sum(self.scenarios_probs) != 1:
            print('ERROR: The sum of scenario probabilities must be 1.')
            return 0
        count_scenarios = np.zeros(len(self.scenarios_files))
        for episode in range(number_of_episodes):
            print('\n ========================= EPISODE# '+str(episode)+' ============================')
            path_to_output = self.path_to_output + 'ArrivalTimes-'+str(episode)+'.csv'  
            
            cumalative_prob = [sum(self.scenarios_probs[:x]) for x in range(1,len(self.scenarios_probs)+1)]
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
     path_to_output = './Episodes/Oversubscription_2/MediumVariance/',
     # Scenarios: Shopping, Working, Driving, Home, Walking
     scenarios_probs = [1.0]).generate_episodes(30)

    return count_scenarios

count_scenarios = test_episode_generator()
print(count_scenarios)

        

    



