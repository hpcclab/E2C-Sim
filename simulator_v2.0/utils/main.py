from Simulator import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

scheduling_method = Config.scheduling_method
train = 0


if scheduling_method == 'TabRLS':
    memory=[]
    if train:
        low = 0
        high = 500
        no_of_iterations = 5

        average_reward = []
        average_reward_per_step = []
        reward_per_step = []    

        plt.figure()
        plt.xlabel('Episode#')
        plt.ylabel('Average Reward per Step')
    else:
        low = 500
        high = 530
        no_of_iterations = 1

if scheduling_method != 'TabRLS':
    low = 500
    high = 530
    no_of_iterations = 1


report_summary = open('./results/'+scheduling_method+'/results-summary.csv','w')
summary_header = ['Episode', 'total_no_of_tasks','mapped', 'offloaded','cancelled','Completion%','xCompletion%','URG_missed','BE_missed','available_energy']
writer = csv.writer(report_summary)
writer.writerow(summary_header)

for i in range(low,high):
    
    s = '\n\n'+ 15 * '='+' EPISODE#'+str(i)+' '+ 15 * '='
    Config.log.write(s)
    print(s)

    total_reward = []
    pbar = tqdm(total=no_of_iterations)

    for k in range(no_of_iterations):
        pbar.update(1)
        Tasks = []
        Config.event_queue.reset()
        Config.current_time = 0.0
        Config.available_energy = Config.total_energy
        Config.cloud.reset()    
        for machine in Config.machines:
            machine.reset()

        path_to_arrival = './Episodes/ArrivalTimes/ArrivalTimes-'+str(i)+'.txt'
        simulation = Simulator(scheduling_method = scheduling_method, path_to_arrival = path_to_arrival, id=i)

        if event.event_type == EventTypes.ARRIVING:  # 1

        simulation.create_event_queue()
        simulation.set_scheduling_method()
        

        if scheduling_method == 'TabRLS':
            simulation.scheduler.train = train
            if k == no_of_iterations -1:
                simulation.scheduler.epsilon = 0.0

        simulation.run()

        if scheduling_method == 'TabRLS' and train:
            df = pd.DataFrame(simulation.scheduler.q_table)
            df.to_csv('./q_table.csv', index= False)
            
            if k == no_of_iterations -1:
                reward_per_step.append(simulation.scheduler.total_reward / simulation.scheduler.steps)
                total_reward.append(simulation.scheduler.total_reward)
            
    if scheduling_method == 'TabRLS' and train:
        average_reward.append(np.mean(total_reward))
        average_reward_per_step.append(np.mean(reward_per_step))


    pbar.close() 


    if scheduling_method == 'TabRLS':     
        memory.append(simulation.scheduler.memory)
        mem = np.array(memory[0][:])
        df_mem = pd.DataFrame(mem)
        df_mem.to_csv('./results/TabRLS/memories/df_mem_'+str(i)+'.csv', index = False)

        if i%10 == 0 and i != low and train:
            iterations = list(range(low,i+1))
            plt.plot(iterations, average_reward_per_step)        
            plt.pause(0.1)  
            plt.savefig('./figures/average_reward_per_step_per_iter.jpg')

    
        
    row = simulation.report('./results/'+scheduling_method+'/')   
    writer.writerows(row)
report_summary.close()
    

