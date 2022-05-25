import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


het_id = 'het-3'

# mu_task = 1.0

v_task = 0.01
mu_machine = 4.0
v_machine = 0.9

no_of_machines = 4
no_of_tasks = 4




def uniform(mu_task, v_task, v_machine, no_of_machines, no_of_tasks):

    machines = [f'M{i}' for i in range(no_of_machines)]
    tasks = [f'T{i}' for i in range(no_of_tasks)]
    etc = pd.DataFrame(data=  None, columns = machines, index = tasks )

    a_task = mu_task*(1-v_task*np.sqrt(3))
    b_task = 2*mu_task - a_task

    for t_id in range(no_of_tasks):
        q = np.random.uniform(a_task, b_task)   
        print(a_task, b_task, q)
        for m_id in range(no_of_machines):
            a_machine = q * (1-v_machine*np.sqrt(3))
            b_machine = 2*q - a_machine

            entry = np.random.uniform(a_machine, b_machine)
            entry = round(entry, 3)
            etc.loc[f'T{t_id}',f'M{m_id}'] = entry
    
    return etc


def gamma(mu_machine,v_machine, v_task, no_of_machines, no_of_tasks):

    machines = [f'M{i}' for i in range(no_of_machines)]
    tasks = [f'T{i}' for i in range(no_of_tasks)]
    etc = pd.DataFrame(data=  None, columns = machines, index = tasks )

    alpha_task = 1 / (v_task * v_task)
    alpha_machine = 1 / (v_machine * v_machine)
    beta_machine =  mu_machine / alpha_machine

    # s = np.random.gamma(alpha_machine, beta_machine, 10000)  
    # plt.figure()
    # plt.hist(s, 100, density = True)
    # plt.show()

    for m_id in range(no_of_machines):
        p = np.random.gamma(alpha_machine, beta_machine)
        beta_task = p / alpha_task

        for t_id in range(no_of_tasks):
            # print(alpha_task, beta_task)
            # s = np.random.gamma(alpha_task, beta_task, 10000)  
            # plt.figure()
            # plt.hist(s, 100, density = True, color='r')
            # plt.show()
            entry = np.random.gamma(alpha_task, beta_task)
            entry = round(entry, 3)
            etc.loc[f'T{t_id}',f'M{m_id}'] = entry
    
    return etc

etc  = gamma(mu_machine, v_machine, v_task, no_of_machines, no_of_tasks)
print(etc)
etc.to_csv(f'../workload/execution_times/etc-{het_id}.csv')






