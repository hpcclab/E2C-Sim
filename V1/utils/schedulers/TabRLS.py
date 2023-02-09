"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""
import heapq
from utils.event import Event, EventTypes
from utils.base_task import TaskStatus, UrgencyLevel
from utils.base_scheduler import BaseScheduler
import Config
from utils.task import Task
from collections import deque 

import numpy as np
import random
import csv
import pandas as pd
from math import ceil
from os.path import isfile
from enum import Enum, unique


class TabRLS(BaseScheduler):

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.name = 'TabRLS'
        self.train = 1
        self.total_no_of_tasks = total_no_of_tasks
        #self.memory = deque(maxlen=1800)
        self.memory = []
        self.gamma = 0.1  # discount rate
        if self.train:
            self.epsilon = 0.99  # exploration rate
        else:
            self.epsilon = 0.0  # exploration rate
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.98
        self.step_size = 0.99
        
        self.steps = 0
        
        
        self.action_size = ( Config.no_of_machines + 1) * self.batch_queue_size
        self.state = 0        
                
        # self.df_states = pd.read_csv('./states.csv')
        # self.states_table = (self.df_states.values).tolist()
        self.states_table = self.read_states()
        
        self.no_of_states = len(self.states_table)
        
        self.rewards = []
        self.done = False
        self.res_val = 0 
        

        if isfile('./q_table.csv'):
            df = pd.read_csv('./q_table.csv')
            self.q_table = df.values
        else:
            self.q_table = np.zeros((self.no_of_states,self.action_size))

        self.q_table_old = None   
        
    
    def read_states(self,path='./states.csv'):
        df = pd.read_csv(path)
        states = df.values.tolist()


        return  states


    def feed(self):

        while (self.unlimited_queue and (-1 in self.batch_queue)):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task


    def choose(self, index):
               
        if self.batch_queue[index] != -1:
            self.unmapped_task = self.batch_queue[index]
            self.batch_queue = self.batch_queue[:index] + self.batch_queue[index+1:]+[-1]            
            #self.feed()
            return self.unmapped_task                         
        else:            
            self.unmapped_task = -1
            return -1
    

    def insert(self, index, task):

        if self.batch_queue[index] != -1:

            if self.batch_queue[-1] != -1:
                popped_task = self.batch_queue[-1]
                self.unlimited_queue.append(popped_task)
                self.batch_queue[-1]= -1
            self.batch_queue = self.batch_queue[:index] + [task] + self.batch_queue[index:-1]

        else:
            self.batch_queue[index] = task



    

    def offload(self, task):
        reward = Config.cloud.admit(task)
        self.stats['offloaded'].append(task)
        nxt_state = self.get_state()
            
        return nxt_state, reward
    
    def no_action(self):
        nxt_state = self.encode_state()
        reward = 0.0

        return nxt_state, reward



    
    def defer(self,task):
        # if task.urgency == UrgencyLevel.BESTEFFORT:
        #     if Config.current_time > task.deadline + task.devaluation_window:
        #         nxt_state, reward = self.drop(task)
        #         return nxt_state, reward
        # elif task.urgency == UrgencyLevel.URGENT:
        #     if Config.current_time > task.deadline:
        #         nxt_state, reward = self.drop(task)
        #         return nxt_state, reward
        
        if -1 in self.batch_queue:
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task
        else:
            replaced_task = self.batch_queue[-1]
            self.unlimited_queue = [replaced_task] + self.unlimited_queue
            self.batch_queue[-1] = task
        task.status =  TaskStatus.DEFERRED
        self.stats['deferred'].append(task)
        self.unmapped_task = -1
        task.no_of_deferring += 1 
        reward = -0.1 * pow(2, task.no_of_deferring)
        nxt_state = self.encode_state()
        
        s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
           task.id, Config.current_time        )
        Config.log.write(s)
        s = 'Batch Queue: \n Head --> [ '
        for task in self.batch_queue:
            if task != -1:
                s += str(task.id)
            else:
                s += '-1'
            s += ' ,'
        s += ']\n'
        Config.log.write(s)
        #print(s)

        return nxt_state, reward


    def drop(self, task):        
        task.status = TaskStatus.CANCELLED
        task.drop_time = Config.current_time
        self.stats['dropped'].append(task)
        self.unmapped_task = -1
        if task.urgency == UrgencyLevel.BESTEFFORT:
            reward = -1
        else:
            reward = -10
        
        nxt_state = self.encode_state()
        s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
            task.id, Config.current_time        )
        Config.log.write(s)
        #print(s)
        
        return nxt_state, reward

    def map(self, selected_task_index, machine):
        
           
        #reward = machine.admit(self.unmapped_task)
        gain, loss = machine.admit(self.unmapped_task)

       
        #if  reward == 'notEmpty' :
        if  gain == 'notEmpty' :
            #print("WARNING: machine "+ str(machine.id) +
            #" cannot admit Task "+ str(self.unmapped_task.id))
            # nxt_state, _ = self.defer(self.unmapped_task)            
            # reward = -1            
            self.insert(selected_task_index, self.unmapped_task)
            self.unmapped_task = -1
            nxt_state = self.encode_state()
            reward = -10.0
            
        else:
            reward = gain - loss            
            self.unmapped_task.assigned_machine = machine            
            self.stats['mapped'].append(self.unmapped_task)
            self.unmapped_task = -1           
            nxt_state = self.encode_state()            

        return nxt_state, reward, gain, loss


    def encode_state(self):
        state = []
        for task in reversed(self.batch_queue):
            if task != -1 :
                state.append(task.type.id)
            else:
                state.append(-1)
        
        
        
        for machine in Config.machines:            
            
            for task in reversed(machine.queue):
                if task != -1:
                    state.append(task.type.id)
                else:
                    state.append(-1)
                    
            running_task = machine.running_task[0]    
            if running_task != -1:
                state.append(running_task.type.id)
                execution_time = running_task.execution_time[machine.type.name]
                progress = (Config.current_time - running_task.start_time) / execution_time
                if progress <= 0.25:
                    state.append(0)
                elif progress >0.25 and progress <=0.5:
                    state.append(1)
                elif progress > 0.5 and progress <= 0.75:
                    state.append(2)
                else:
                    state.append(3)
            else:
                state.append(-1)
                state.append(-1)
            
        energy_level = Config.available_energy / Config.total_energy

        if energy_level <= 0.25:
            state.append(0)
        elif energy_level > 0.25 and energy_level <= 0.5:
            state.append(1)
        elif energy_level > 0.5 and energy_level <= 0.75:
            state.append(2)
        else:
            state.append(3)
        
        state_id = self.states_table.index(state)

        #state_id = self.df_states[((self.df_states==state).all(1))].index.values[0]

        return state_id
    
    def reset(self):
        for machine in Config.machines:
            machine.reset()
        
        self.state = self.encode_state()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def act(self):

        state = self.encode_state()             
        if np.random.random() <= self.epsilon:        
            action = random.randrange(self.action_size)
            #print('non-greed --> A:{} S:{} action_size: {}'.format(action,state,self.action_size))
        else:                       
            action =  np.argmax(self.q_table[state])
            #print('greed --> A:{} S:{}'.format(action,state))
            

        return action

    def step(self, action):

        state = self.encode_state()
        gain = None
        loss = None

        if action < self.action_size-self.batch_queue_size:
            assigned_machine = action % Config.no_of_machines # starts with zero
            selected_task_index = action // Config.no_of_machines 
            selected_task = self.choose(selected_task_index)
            if selected_task != -1:
                nxt_state, reward, gain, loss = self.map(selected_task_index, Config.machines[assigned_machine])
            else:
                nxt_state = state
                reward = -10.0
        else:
            selected_task_index = action - ( Config.no_of_machines * self.batch_queue_size)
            selected_task = self.choose(selected_task_index)
            if selected_task != -1:
                nxt_state, reward = self.defer(self.unmapped_task)
            else:
                nxt_state = state
                reward = -10.0
    
        if self.train:                     
            self.q_table[state][action] += self.step_size * ( reward + self.gamma * np.argmax(self.q_table[nxt_state]) - self.q_table[state][action])
            
            
        self.rewards.append(reward)
       
        # if action == 0 :
        #     print('defer -->>')
        #     nxt_state, reward = self.defer(self.unmapped_task)
        # elif action in list(range(1, Config.no_of_machines +1 )):
        #     print('map -->> {}'.format(action))
        #     nxt_state, reward = self.map(Config.machines[action-1])
        # elif action == Config.no_of_machines +1:
        #     print('Cancel -->>')
        #     nxt_state, reward = self.drop(self.unmapped_task)
        


        #if self.steps < self.total_no_of_tasks and Config.available_energy > 0:
        if Config.available_energy > 0:
            #self.steps +=1 
            done = False
        else:
            done = True
        self.steps += 1 
        # done = False
        #s = '\nAction: {}  Reward: {} '. format(action, reward)
        #print(s)
        Config.history_writer.writerow([action, reward, gain, loss])
        
       
        return nxt_state, reward, done



##############################################
    
    def schedule(self):

        # if self.choose() == -1:            
        #     return -1
        enable = False
        for task in self.batch_queue:
            if task != -1:
                enable = True
        
        if not enable: 
            return      
        action = self.act()
        state = self.encode_state()               
        nxt_state, reward, done = self.step(action)          
        self.remember(state, action, reward, nxt_state, done)
       

    def residual(self, q_old, q_new):

        n = self.no_of_states * self.action_size
        res = np.power(q_new- q_old , 2)        
        res = np.sqrt(np.sum(res)/n)
    
        return res

        


    



