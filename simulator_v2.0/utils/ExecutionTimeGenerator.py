import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



#def generate(miu, sigma, size):
def generate(low, high, size):
        
        #distribution = np.random.normal(miu, sigma, size)     

        distribution = np.random.uniform(low, high, size)        
        distribution = [round(x, 3) for x in distribution]

        return distribution

def write(distribution, task_type, machine_type, path):
    file_name = '{}-{}.csv'.format(task_type, machine_type)
    with open(path+file_name,'w') as outfile:
        for row in distribution:
            outfile.writelines(str(row)+'\n')
    


dis = generate(1.0, 1.2, 1000)
write(dis, 2, 'CLOUD', './synthetic_execution_time/medium-variance/')



