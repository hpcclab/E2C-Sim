"""
Authors: Ali Mokhtari
Created on Jan. 07, 2021.

Simulator is used to set and get current time.

"""

class Simulator:
    
    current_time = [0.0]
    
    def set_current_time(self, time):
        self.current_time[0] = time
        
    def get_current_time(self):
        return self.current_time[0]

