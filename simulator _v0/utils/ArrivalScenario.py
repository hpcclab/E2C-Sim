'''
Authors: Ali Mokhtari
Created on Dec. 24, 2020.

Here, an arrival scenario for task types in given time interval is 
defined. This class is used to generate arrival times distribution
for task types that are arriving to the system considering different
scenarios. For example, in "shopping" scenario, we may have different
tasks arrival from a scenario considering "staying in office".

'''

from  ArrivalPattern import *


class ArrivalScenario:
    # The arrival scenario with the name of "scenario_name" starts at
    # scenario_start_time and ends at scenario_end_time.
        
    
    
    def __init__(self, scenario_name, scenario_start_time, scenario_end_time):
        self.scenario_name = scenario_name
        self.scenario_start_time = scenario_start_time
        self.scenario_end_time = scenario_end_time
        self.arrival_times = {}
        
    def add_task_arrival(self, task_type_ID, pattern, no_of_tasks):
        # This method adds the arrival times of a task to the arrival_times
        # of the ArrivalScenario.
        # The arrival times of the task_type_ID, arrival_times[task_type_ID],
        # has the lenght of no_of_tasks and pattern of "pattern".
        arrival_pattern = ArrivalPattern(pattern, 
                                        self.scenario_start_time,
                                        self.scenario_end_time, no_of_tasks)
        self.arrival_times[task_type_ID] = arrival_pattern.arrival_generator()
        
        return self.arrival_times[task_type_ID]
    
    
def test():
    # A test for debugging
    sc_shopping = ArrivalScenario('shopping', 0, 600)
    sc_shopping.add_task_arrival(1,'uniform',600)
    sc_shopping.add_task_arrival(2,'normal',600)
    sc_shopping.add_task_arrival(3,'spiky',600)     
    sns.displot(sc_shopping.arrival_times, kind = 'ecdf' )
    plt.show()    
    plt.figure()
    sns.displot(sc_shopping.arrival_times, kind = 'kde' , fill = True )
    plt.show()
    
    return sc_shopping.arrival_times

#Just for test
# test()
   
    
        
        