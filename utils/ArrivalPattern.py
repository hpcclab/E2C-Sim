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
    # Using method in this class, the distribution of tasks arrival times
    # in the speicified interval of time is generated. 
    # The time interval begins at start_time and ends at end_time.
    # no_of_tasks arrive to the system during this time interval. So,
    # the length of arrival times distribution should be no_of_tasks.
    # It means that for each task, an arrival time is generated.
    
    
    def uniform(self, start_time, end_time, no_of_tasks):
        # Here, a sample of arrival times are drawn from the uniform
        # distribution. In other words, any value within the given
        # interval is equally likely to be drawn by uniform sampling.
        
        distribution = np.random.uniform(start_time, end_time, no_of_tasks)        
        return distribution
    
    
    def normal(self, start_time, end_time, no_of_tasks):
        # Here, a sample of arrival times are drawn from the normal
        # distribution. 
        # the mean of the normal distribution is considered to be
        # in the middle of start_time and end_time.
        # Also, the standard deviation is considered in a way that
        # the given time interval located in 6 standard deviations.
        # <start_tim-------- 6 sigma --------- end_time> 
        mu = (start_time + end_time) / 2.0
        sigma = (end_time - start_time) / 6.0             
        
        distribution = np.random.normal(mu, sigma, no_of_tasks)
        # The distribution is truncated to fit the given timeinterval.
        distribution[distribution > end_time] =end_time
        distribution[distribution < start_time] = start_time
        
        return distribution
        
    
    def exponential(self, start_time, end_time, no_of_tasks):
        # Here, a sample of arrival times are drawn from the exponential
        # distribution. 
        # the scale parameter (beta) of exponential distribution is 
        # considered in a way that the possibility of the arriving time  
        # of a task being less than the end_time is 99.9%.         
        # CDF = 1 - exp(-time_interval/beta) = 0.999 
        # --> beta = time_interval / ln(1000)
        beta = (end_time - start_time) / np.log(1000)
        # The distribution is shifted to start_time.
        distribution = start_time + np.random.exponential(beta, no_of_tasks)
        # The distribution is truncated to fit the given time interval.
        distribution[distribution > end_time] = end_time
        
        return distribution
    
    def spiky(self, start_time, end_time, no_of_tasks, no_of_spikes = 10):
        # Here, tasks are considered to be arrived in spiky manner. The spikes
        # occured at random positions but have same width.
        # The number of tasks arrive at each spike is also a random variable.
        # no_of_spikes: It is the number of spikes in the given time
        # interval [start_time, end_time]
        
        # Each spike width is 1% of the time interval.
        spike_width = 0.01 * (end_time - start_time)   
        # Each spike begins at a random position which is drawn from a 
        # uniform distribution.
        spike_starts = np.random.uniform(start_time , end_time, no_of_spikes)
        
        distribution = []
        # remaining_tasks is the number of tasks that arrive afterward.       
        remaining_tasks = no_of_tasks
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
    
    uniform = ArrivalPattern().uniform(10,30,1000)
    normal = ArrivalPattern().normal(10,30,1000)
    exponential = ArrivalPattern().exponential(10, 30, 1000)
    spiky = ArrivalPattern().spiky(10, 30, 1000)
    
    data = {'uniform':uniform, 'normal': normal, 'exponential':exponential,
            'spiky':spiky}      
       
    sns.displot(data, kind = 'ecdf' )
    plt.show()
    
    plt.figure()
    sns.displot(data, kind = 'kde' , fill = True )
    plt.show()
       
    return data
    
data = test()