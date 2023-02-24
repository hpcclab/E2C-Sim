"""
Authors: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 24, 2022
"""

class Time:


    def __init__(self):
        self.current_time = 0.0

    

    def gct(self):
        return self.current_time
    
    def sct(self,time):
        self.current_time = time
    
    def reset(self):
        self.current_time = 0.0
    