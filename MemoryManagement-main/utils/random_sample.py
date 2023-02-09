"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022

"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys


class RandomSample:
    

    def __init__(self):
        self.distributions = ['uniform', 'normal', 'interarrival', 'spiky']

    def generate(self,dist, start, end, no_of_requests):        
        
        try:
            assert(dist in self.distributions ), f'ERROR: The distribution {dist} used to sample launch times is unknown'
        except AssertionError as err:
            print(err)
            sys.exit()
        
        if dist == 'uniform':
            distribution = self.uniform(start, end, no_of_requests)

        elif dist == 'normal':
            distribution = self.normal(start, end, no_of_requests)

        elif dist == 'interarrival':
            distribution = self.interarrival(start, end, no_of_requests)

        elif dist == 'spiky':
            distribution = self.spiky(start, end, no_of_requests)
    
        return distribution

    def uniform(self,start, end, no_of_requests):        

        distribution = np.random.uniform(start, end, no_of_requests)
        distribution = [round(x, 3) for x in distribution]

        return distribution

    def normal(self, start, end, no_of_requests):        
        mu = (start + end) / 2.0
        sigma = (end - start) / 6.0

        distribution = np.random.normal(mu, sigma, no_of_requests)
        # The distribution is truncated to fit the given timeinterval.
        distribution[distribution > end] = end
        distribution[distribution < start] = start
        distribution = [round(x, 3) for x in distribution]

        return distribution

    
    def interarrival(self,start, end, no_of_requests):
                
        beta = (end - start) / no_of_requests 
        interarrivals = np.random.exponential(beta, no_of_requests)
        distribution = start + np.cumsum(interarrivals)        
        distribution = [round(x, 3) for x in distribution]

        return distribution

    def spiky(self,start, end, no_of_requests, no_of_spikes=10):
       
        spike_width = 0.01 * (end - start)
        
        try:
            assert(isinstance(no_of_spikes, int)), "Invalid amount of spikes."
            
        except AssertionError as err:
            print(err)
            sys.exit()
        
        spike_starts = np.random.uniform(start,end, no_of_spikes)
        distribution = []
        # remaining_tasks is the number of tasks that arrive afterward.
        remaining_tasks = no_of_requests
        # A loop to generate spikes sequentially
        for spikes_no in range(no_of_spikes):
            # no_of_tasks_in_spike: Number of tasks arrive at each spike
            no_of_requests_in_spike = np.random.randint(remaining_tasks + 1)
            # spike: distribution of tasks arrival time in each spike
            spike = np.random.uniform(spike_starts[spikes_no],
                                        spike_starts[spikes_no] + spike_width,
                                        no_of_requests_in_spike)
            remaining_tasks -= no_of_requests_in_spike
            distribution = np.concatenate((distribution, spike))
        distribution = [round(x, 3) for x in distribution]

        return distribution


def test():
    rnd_sample = RandomSample()
    uniform = rnd_sample.generate('uniform', 10, 30, 1000)
    normal = rnd_sample.generate('normal', 10, 30, 1000)
    exponential = rnd_sample.generate('interarrival', 10, 30, 1000)
    spiky = rnd_sample.generate('spiky', 10, 30, 1000)

    data = {'uniform': uniform, 'normal': normal, 'interarrival': exponential,
            'spiky': spiky}
       
    sns.displot(data, kind='kde', fill=True)
    plt.show()

    return data

# test

if __name__ == '__main__':
    data = test()
