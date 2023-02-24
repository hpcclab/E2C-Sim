"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022

"""


class Time:

    def __init__(self):
        self.current_time = 0

    
    def get_time(self):
        return self.current_time
    
    def set_time(self, t):
        self.current_time = t
