import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

def estimate_deadline(path_to_file, epsilon):        
    
    data = []    
    with open(path_to_file, 'r') as file:
        
        rows = file.readlines()      
        count = 0
        for row in rows: 
            if count != 0:
                data.append(float(row.rstrip()))
            count+=1
            
    
    data = np.array(data)
    Q1 = np.percentile(data, 25, interpolation='midpoint')
    Q1 = np.percentile(data, 50, interpolation='midpoint')
    Q3 = np.percentile(data, 75, interpolation='midpoint')
    IQ = Q3 - Q1
    data = data[np.where(data > Q1-1.5*IQ )]
    data = data[np.where(data < Q3+1.5*IQ )]
    plt.hist(data, bins=30)
    plt.show()
    plt.boxplot(data, vert=False)
    df = pd.DataFrame(data, columns=['execution_time'])
    df.to_csv(filename, index=False)
    deadline = epsilon * np.mean(data) +  np.max(data)
    print('Suggested deadline: {}'.format(deadline))
    
    return data, deadline

filename = '3-g3s_xlarge.csv'            
data, deadline = estimate_deadline(filename, 2)
