"""
Authors: Ali Mokhtari
Created on Jan. 17, 2021.

This module is to read and set configuration parameters. These parameters
are read from 'config.txt' and 'setting.txt' files. 
"""

# Program Settings:
# queue_length: An integer number inidicates the length of machine queue
# machine_types: A list of machine types
# task_types: A list of task types
# All parameters are set to None initially.
queue_length = None
machine_types = None
task_types = None


def init():
    # This function is used to initially set the configuration parameters
    # at the beginning of the main module.
    global queue_length 
    global machine_types 
    global task_types
    
    set_config()
    
    

def set_config(path = './config.txt'):
    # This function read configuration parameters from the file directed
    # by the path and assign their values to the global variables.  
    global queue_length 
    global machine_types 
    global task_types
    
    with open(path,'r') as config:            
        for line in config:
            if line[0] == '$':
                var = line.split('=')[0].split('$')[1].strip()                
                if var == 'queue_length' :
                    val = line.split('=')[1].strip()
                    queue_length = int(val)
                    print('queue_length = '+ str(queue_length))
                                        
                elif var == 'machine_types':
                    val = line.split('=')[1].strip().strip('][').split(',')
                    machine_types = val
                    print('machine_types = '+ str(machine_types))
                    
                elif var == 'task_types':
                    val = line.split('=')[1].strip().strip('][').split(',')
                    task_types = val
                    print('machine_types = '+ str(task_types))
                    
                else:
                    print('Error: The configuration parameter does not match!')