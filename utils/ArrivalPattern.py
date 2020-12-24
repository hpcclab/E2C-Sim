'''
Authors: Ali Mokhtari
Created on Dec. 22, 2020.

In simulation, the arrival of tasks needs to be also simulated. Here,
different patterns of arrival are considered. In each pattern, a time
distribution that indicates the arrival time of the tasks in the
specified interval of time is generated.
"uniform", "normal", "exponential", and "spiky" pattern are considered.

'''

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class ArrivalPattern:
    # Using this class, a pattern (distribution) is used to generate the
    # arrival times. 
    # Each arrival pattern begins at start_time and ends at end_time.
    # During this time interval, the number of tasks that arrive to the 
    # system is no_of_tasks.
    # To generate the arrival times, a sample of size no_of_tasks is
    # drawn from the pattern.
    
    def __init__(self, pattern, start_time, end_time, no_of_tasks):
        self.pattern = pattern
        self.start_time = start_time
        self.end_time = end_time
        self.no_of_tasks = no_of_tasks
        
    
    def arrival_generator(self):
        # It generates the arrival times distribution based on arrival
        # pattern, time interval, and no_of_tasks arrive.
        # len(distribution) is no_of_tasks.
        
        if self.pattern == 'uniform':
            distribution = self.uniform()
        
        elif self.pattern == 'normal':
            distribution = self.normal()
        
        elif self.pattern == 'exponential':
            distribution = self.exponential()
        
        elif self.pattern == 'spiky':
            distribution = self.spiky()
        
        
        return distribution
    
    def uniform(self):
        # Here, a sample of arrival times are drawn from the uniform
        # distribution. In other words, any value within the given
        # interval is equally likely to be drawn by uniform sampling.
        
        distribution = np.random.uniform(self.start_time, self.end_time,
                                         self.no_of_tasks)        
        return distribution
    
    
    def normal(self):
        # Here, a sample of arrival times are drawn from the normal
        # distribution. 
        # the mean of the normal distribution is considered to be
        # in the middle of start_time and end_time.
        # Also, the standard deviation is considered in a way that
        # the given time interval located in 6 standard deviations.
        # <start_tim-------- 6 sigma --------- end_time> 
        mu = (self.start_time + self.end_time) / 2.0
        sigma = (self.end_time - self.start_time) / 6.0             
        
        distribution = np.random.normal(mu, sigma, self.no_of_tasks)
        # The distribution is truncated to fit the given timeinterval.
        distribution[distribution > self.end_time] =self.end_time
        distribution[distribution < self.start_time] = self.start_time
        
        return distribution
        
    
    def exponential(self):
        # Here, a sample of arrival times are drawn from the exponential
        # distribution. 
        # the scale parameter (beta) of exponential distribution is 
        # considered in a way that the possibility of the arriving time  
        # of a task being less than the end_time is 99.9%.         
        # CDF = 1 - exp(-time_interval/beta) = 0.999 
        # --> beta = time_interval / ln(1000)
        beta = (self.end_time - self.start_time) / np.log(1000)
        # The distribution is shifted to start_time.
        distribution = self.start_time + np.random.exponential(
            beta, self.no_of_tasks)
        # The distribution is truncated to fit the given time interval.
        distribution[distribution > self.end_time] = self.end_time
        
        return distribution
    
    def spiky(self, no_of_spikes = 10):
        # Here, tasks are considered to be arrived in spiky manner. The spikes
        # occured at random positions but have same width.
        # The number of tasks arrive at each spike is also a random variable.
        # no_of_spikes: It is the number of spikes in the given time
        # interval [start_time, end_time]
        
        # Each spike width is 1% of the time interval.
        spike_width = 0.01 * (self.end_time - self.start_time)   
        # Each spike begins at a random position which is drawn from a 
        # uniform distribution.
        spike_starts = np.random.uniform(self.start_time , 
                                         self.end_time, no_of_spikes)
        
        distribution = []
        # remaining_tasks is the number of tasks that arrive afterward.       
        remaining_tasks = self.no_of_tasks
        # A loop to generate spikes sequentially
        for spikes_no in range(no_of_spikes):
            # no_of_tasks_in_spike: Number of tasks arrive at each spike
            no_of_tasks_in_spike = np.random.randint(remaining_tasks)
            # spike: distribution of tasks arrival time in each spike
            spike = np.random.uniform(spike_starts[spikes_no], 
                                      spike_starts[spikes_no]+spike_width,
                                      no_of_tasks_in_spike)
            remaining_tasks -= no_of_tasks_in_spike
            distribution = np.concatenate((distribution,spike))
        
        return distribution
            
    
def test():
    
    uniform = ArrivalPattern('uniform',10,30,1000).arrival_generator()
    normal = ArrivalPattern('normal',10,30,1000).arrival_generator()
    exponential = ArrivalPattern('exponential',10,30,1000).arrival_generator()
    spiky = ArrivalPattern('spiky',10,30,1000).arrival_generator()
    
    data = {'uniform':uniform, 'normal': normal, 'exponential':exponential,
            'spiky':spiky}      
       
    sns.displot(data, kind = 'ecdf' )
    plt.show()
    
    plt.figure()
    sns.displot(data, kind = 'kde' , fill = True )
    plt.show()
       
    return data

# Just for Test -->
#data = test()