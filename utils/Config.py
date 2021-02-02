"""
Author: Ali Mokhtari
Created on Jan. 27, 2021.

This module reads configuration parameters from the json file. 

"""
import json


def read_config(path = './config.txt'):
    # This function read configuration parameters from the json file 
    # located in path      
        
    with open(path) as f: 
        data = f.read()    
    # reconstructing the data as a dictionary 
    config = json.loads(data)
    
    return config