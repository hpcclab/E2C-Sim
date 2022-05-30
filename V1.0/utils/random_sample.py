"""
Authors: Ali Mokhtari
Created on Dec. 22, 2020.

Description:


"""
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class RandomSample:    

    def __init__(self, start_time, end_time, no_of_tasks, seed = 100):        
        self.start_time = start_time
        self.end_time = end_time
        self.no_of_tasks = no_of_tasks
        self.seed = seed

    def generate(self, pattern):

        self.pattern = pattern  
        np.random.seed(self.seed)      
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
        distribution = np.random.uniform(self.start_time, self.end_time,
                                         self.no_of_tasks)
        distribution = [round(x, 3) for x in distribution]

        return distribution

    def normal(self):       
        mu = (self.start_time + self.end_time) / 2.0
        sigma = (self.end_time - self.start_time) / 6.0

        distribution = np.random.normal(mu, sigma, self.no_of_tasks)       
        distribution[distribution > self.end_time] = self.end_time
        distribution[distribution < self.start_time] = self.start_time
        distribution = [round(x, 3) for x in distribution]

        return distribution

    def exponential(self):
        
        beta = (self.end_time - self.start_time) / self.no_of_tasks
        interarrival = np.random.exponential(
            beta, self.no_of_tasks)
        distribution = self.start_time + np.cumsum(interarrival)        
        distribution = [round(x, 3) for x in distribution]

        return distribution

    def spiky(self, no_of_spikes=10):
        # Here, tasks are considered to be arrived in spiky manner. The spikes
        # occurred at random positions but have same width.
        # The number of tasks arrive at each spike is also a random variable.
        # no_of_spikes: It is the number of spikes in the given time
        # interval [start_time, end_time]

        # Each spike width is 1% of the time interval.
        spike_width = 0.01 * (self.end_time - self.start_time)
        # Each spike begins at a random position which is drawn from a 
        # uniform distribution.
        if isinstance(no_of_spikes, int):
            spike_starts = np.random.uniform(self.start_time,
                                             self.end_time, no_of_spikes)
            distribution = []
            # remaining_tasks is the number of tasks that arrive afterward.
            remaining_tasks = self.no_of_tasks
            # A loop to generate spikes sequentially
            for spikes_no in range(no_of_spikes):
                # no_of_tasks_in_spike: Number of tasks arrive at each spike
                no_of_tasks_in_spike = np.random.randint(remaining_tasks + 1)
                # spike: distribution of tasks arrival time in each spike
                spike = np.random.uniform(spike_starts[spikes_no],
                                          spike_starts[spikes_no] + spike_width,
                                          no_of_tasks_in_spike)
                remaining_tasks -= no_of_tasks_in_spike
                distribution = np.concatenate((distribution, spike))
            distribution = [round(x, 3) for x in distribution]

            return distribution
        else:
            print("Invalid amount of spikes.")
            sys.exit()
            
            


def test():
    uniform = ArrivalPattern(10, 30, 1000).generate('uniform')
    normal = ArrivalPattern(10, 30, 1000).generate('normal')
    exponential = ArrivalPattern(10, 30, 1000).generate('exponential')
    spiky = ArrivalPattern(10, 30, 1000).generate('spiky')

    data = {'uniform': uniform, 'normal': normal, 'exponential': exponential,
            'spiky': spiky}
    
    sns.displot(data, kind='kde', fill=True)
    plt.show()
    return data

# Just for Test -->
# data = test()
