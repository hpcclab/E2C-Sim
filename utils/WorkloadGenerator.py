'''
Authors: Ali Mokhtari
Created on Jan. 01, 2021.

Here, The details of scenarios are read from "Scenarios.txt" , then, the
arrival times of tasks along with their task types  are written to 
"ArrivalTimes.txt" file. Tasks in "ArrivalTimes.txt" are sorted based on
the values of the arrival times.

'''

from ArrivalScenario import *


class Workload:
    # The Workload class read scenarios from the file in path_to_scenarios.
    # Then, the arrival times of tasks and their task types are written to
    # "ArrivalTimes.txt" located in path_to_output.
    
    def __init__(self,path_to_scenarios='./',
                 path_to_output='./'):
        self.path_to_scenarios = path_to_scenarios
        self.path_to_output = path_to_output
    
    def read_scenarios(self):
        # This method is used to read details of scenarios from Scenarios.txt
        # located in path_to_scenarios.
        
        # "scenarios" is a list of list each contains the name, 
        # start_time, and end_time of each scenario.
        # "scenario_tasks" is a list of list each contains the
        # task_type_id, pattern, and no_of_tasks considered in
        # scenario which is stored in the "scenarios".
        # "tasks" is a list contains [task_type_id, pattern, no_of_tasks].
        scenarios = []
        scenario_tasks=[]
        tasks = []
        
        with open(self.path_to_scenarios+
                  'Scenarios.txt', 'r') as scenario_file:
            
            data = scenario_file.readlines()
            
            for lines in data:                
                lines = lines.strip()
                # check the line is not neither a comment or details of
                # tasks.
                if lines[0] != '#' and lines[:2] != '__':
                    name = lines.split(',')[0].strip()
                    start_time = float(lines.split(',')[1])
                    end_time = float(lines.split(',')[2])
                    scenarios.append([name,start_time,end_time])
                    
                    # When the code reaches to a new scenario, the tasks
                    # list which has already read and stored in tasks list
                    # is appeneded to scenario_tasks list.
                    # Then, the tasks list is initialized to empty list for
                    # the next scenario.
                    # In case of first scenario, tasks list is empty and 
                    # if condition is False.
                    if tasks:                        
                        scenario_tasks.append(tasks)
                        tasks = []
                # All tasks detail begin with "__". 
                if lines[:2] == '__':
                    task_type_ID = int(lines.split(',')[1])                    
                    pattern = lines.split(',')[2].strip()
                    no_of_tasks = int(lines.split(',')[3])
                    tasks.append([task_type_ID, pattern, no_of_tasks])
                    
            scenario_tasks.append(tasks)
                    
        return scenarios,scenario_tasks
    
    
    def scenarios_arrival_times(self,scenarios, scenario_tasks):
        # This method takes scenarios and scenario_tasks and output the
        # arrival_times for tasks for each scenario in scenarios.
        # arrival_times is a dictionary with scenarion_name as keys and
        # a dictionary of task types arrival times.
        # arrival_times = {scenario_name:{task_type_id: arrival_time, ...},..}
        
        arrival_times = {}
        
        for scenario_number in range (len(scenarios)):
            
            scenario_name = scenarios[scenario_number][0]
            scenario_start_time = scenarios[scenario_number][1]
            scenario_end_time = scenarios[scenario_number][2]
            
            print('\n Scenario '+ scenario_name + 'is created ...')
            print('\t'+scenario_name+ ' starts at ' +
                  str(scenario_start_time) +' sec and ends at '+
                  str(scenario_end_time) +' sec')
            
            arrival_scenario = ArrivalScenario(scenario_name,
                                               scenario_start_time,
                                               scenario_end_time)
            
            for task in scenario_tasks[scenario_number]:
                task_type_ID = task[0]
                pattern = task[1]                
                no_of_tasks = task[2]
                print( '\t\t task type '+str(task_type_ID)+ 
                      ' with "'+pattern+ '" pattern and '+str(no_of_tasks)+
                      ' tasks is added to '+ scenario_name+ ' scenario')                
                arrival_scenario.add_task_arrival(task_type_ID,pattern,
                                                  no_of_tasks)                
            arrival_times[scenario_name] = arrival_scenario.arrival_times
            
        return  arrival_times
    
    
    def aggregate_arrival_times(self,arrival_times):
        # This method rearrange the arrival_times in a way that ignore
        # scenario_name and it becomes a dictionary with task_type_id 
        # as keys and arrival times of each task type as its values.
        
        aggregated_arrival_times = {}
        dictionaries = []
        
        for scenario, tasks_arrivals in arrival_times.items():            
            dictionaries.append(tasks_arrivals)            
        
        for task_type_ID in dictionaries[0].keys():
             aggregated_arrival_times[task_type_ID] = np.concatenate(
                 list(d[task_type_ID] for d in dictionaries))
            
        return aggregated_arrival_times
    
        
    def generate(self):        
        scenarios,scenario_tasks = self.read_scenarios()
        arrival_times = self.scenarios_arrival_times(scenarios, scenario_tasks)
        aggregated_arrival_times = self.aggregate_arrival_times(arrival_times)
        
        return aggregated_arrival_times
    
    def write_to_file(self,aggregated_arrival_times):
        # It firstly sort the arrival times of each task type, then
        # the sorted arrival time along with its task type is written
        # to the ArrivalTimes.txt file.
        
        sorted_dict_times = {}
        total_no_of_tasks = 0
        for task_type_ID, arrival_times in aggregated_arrival_times.items():
            arrival_times.sort()            
            sorted_dict_times[task_type_ID] = arrival_times
            total_no_of_tasks += len(arrival_times)      
        
        all_tasks_arrival_times = []
        all_tasks_id = []
        min_id = None
        
        with open(self.path_to_output+'ArrivalTimes.txt','w') as outputfile:
            print("\nWriting arrival times to "+
                  self.path_to_output+'ArrivalTimes.txt ===>>>'+ 
                  " Total Number of Tasks = "+str(total_no_of_tasks))
            
            for count_task in range(0,total_no_of_tasks):
                min_arrival_times = float('inf')                
                for task_type_ID in sorted_dict_times.keys():
                    arr_tt = sorted_dict_times[task_type_ID]                    
                    if len(arr_tt) and min_arrival_times > arr_tt[0] :
                        min_arrival_times = arr_tt[0]
                        min_id = task_type_ID                    
                all_tasks_arrival_times.append(min_arrival_times)
                all_tasks_id.append(min_id)
                outputfile.writelines(str(min_id)+','+str(min_arrival_times)+
                                      '\n')                
                sorted_dict_times[min_id] = np.delete(sorted_dict_times[min_id],[0])
                
        return all_tasks_arrival_times,all_tasks_id
    
# TEST 
def test():
    aggregated_arrival_times = Workload().generate()
    all_times,all_ids = Workload().write_to_file(aggregated_arrival_times)
    
test()

        