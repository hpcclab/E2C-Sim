"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021

Description:


"""


class Cloud:
    # Description:
    
    def __init__(self, bandwidth, latency):
        raise NotImplementedError
    
    def reset(self):
        # Method Description:
        raise NotImplementedError

    def admit(self, task):
        # Method Description:
        raise NotImplementedError
    
    def terminate(self, task):
        # Method Description:
        raise NotImplementedError
        