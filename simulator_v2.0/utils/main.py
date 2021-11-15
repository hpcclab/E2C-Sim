from Simulator import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

scheduling_method = Config.scheduling_method
variance_level = 'medium'
oversubscription_level = '2'
train = 0


if scheduling_method == 'TabRLS':
    memory=[]
    if train:
        low = 0
        high = 500
        no_of_iterations = 100

        average_reward = []
        average_reward_per_step = []
        reward_per_step = [] 
        residuals = []  
        
    else:
        low = 500
        high = 530
        no_of_iterations = 1

if scheduling_method != 'TabRLS':
    low = 500
    high = 530
    no_of_iterations = 1

path_to_result = './results/oversubscription-{}/{}-variance/{}/'.format(
    oversubscription_level, variance_level,scheduling_method)
report_summary = open(path_to_result+'results-summary.csv','w')
summary_header = ['Episode', 'total_no_of_tasks','mapped', 'offloaded','cancelled','Completion%','xCompletion%','totalCompletion%','URG_missed','BE_missed','consumed_energy%']
writer = csv.writer(report_summary)
writer.writerow(summary_header)

df_task_based_report = pd.DataFrame()

count = 0 

for i in range(low,high):
    
    s = '\n\n'+ 15 * '='+' EPISODE#'+str(i)+' '+ 15 * '='
    Config.log.write(s)
    print(s)

    rewards = []
    pbar = tqdm(total=no_of_iterations)

    
    
    for k in range(no_of_iterations):        
        pbar.update(1)   
        count += 1      
        Tasks = []
        Config.event_queue.reset()
        Config.current_time = 0.0
        Config.available_energy = Config.total_energy
        Config.cloud.reset()    
        for machine in Config.machines:
            machine.reset()

        path_to_arrival = './Episodes/oversubscription-{}/{}-variance/ArrivalTimes-{}.csv'.format(
            oversubscription_level, variance_level,i)
        simulation = Simulator(scheduling_method = scheduling_method, path_to_arrival = path_to_arrival, id=i)  
        simulation.create_event_queue()
        simulation.set_scheduling_method()

        if scheduling_method == 'TabRLS':
            simulation.scheduler.train = train
            if k==0 and train:                
               q_old = simulation.scheduler.q_table.copy()                
                
                
            if k == no_of_iterations -1:
                simulation.scheduler.epsilon = 0.0

        simulation.run()
        
        if scheduling_method == 'TabRLS' and train:            
            df = pd.DataFrame(simulation.scheduler.q_table)
            df.to_csv('./q_table.csv', index= False)
            # res = simulation.scheduler.residual()
            # residuals.append(res)
            rewards.append(np.sum(simulation.scheduler.rewards))            
            
                 
            
    if scheduling_method == 'TabRLS' and train:
        average_reward.append(np.mean(rewards))        
        q_new = simulation.scheduler.q_table.copy()       
        res = simulation.scheduler.residual(q_old,q_new)
        residuals.append(res)


    pbar.close() 


    if scheduling_method == 'TabRLS':     
        memory.append(simulation.scheduler.memory)
        mem = np.array(memory[0][:])
        df_mem = pd.DataFrame(mem)
        df_mem.to_csv(path_to_result+'memories/df_mem_'+str(i)+'.csv', index = False)

        # if i%10 == 0 and i != low and train:
        #     iterations = list(range(low,i+1))
        #     plt.plot(iterations, average_reward_per_step)        
        #     plt.pause(0.1)  
        #     plt.savefig('./figures/average_reward_per_step_per_iter.jpg')
        if i%10 == 0 and i != low and train:
            #iterations = list(range(1,count+1))
            iterations = list(range(low,i+1))
            #plt.plot(iterations, residuals)
            plt.figure(figsize=(24,4))
            plt.plot(iterations, average_reward)
            plt.xlabel('Episode')
            plt.ylabel('Average of Total Reward')
            plt.grid()
            plt.savefig('./figures/residuals.jpg')
            plt.show()
            


    
        
    row, task_report = simulation.report(path_to_result+'/')   
    writer.writerows(row)
    df_task_based_report = df_task_based_report.append(task_report, ignore_index=True)    
report_summary.close()
df_task_based_report.to_csv(path_to_result+'task_based_report.csv', index = False)
df_summary = pd.read_csv(path_to_result+'results-summary.csv', 
usecols=['Completion%', 'xCompletion%', 'totalCompletion%',
'consumed_energy%'])

print('\n\n'+ 10*'*'+'  Task_based Average Results '+10*'*')
print(df_task_based_report.mean())

print('\n\n'+ 10*'*'+'  Average Results of Executing Episodes  '+10*'*')
print(df_summary.mean())


