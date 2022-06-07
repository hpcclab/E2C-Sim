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
from tensorflow.keras import Sequential, initializers
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam, RMSprop

import numpy as np
import random
import csv
import pandas as pd
from math import ceil
from os.path import isfile
from enum import Enum, unique


class RLS(BaseScheduler):

    def __init__(self, total_no_of_tasks):
        super().__init__()
        self.name = 'RLS'
        self.train = 1
        self.total_no_of_tasks = total_no_of_tasks
        self.memory = deque()        
        self.gamma = 0.1  # discount rate
        if self.train:
            self.epsilon = 0.99 # exploration rate
        else:
            self.epsilon = 0.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.95
        self.sample_size = 256
        self.batch_size = 32
        self.train_start = 500
        
        self.steps = 0
        
        self.no_of_TT = len(Config.task_types)
        self.action_size = ( Config.no_of_machines + 2) * self.batch_queue_size 
        s =  self.batch_queue_size + Config.no_of_machines * (Config.queue_size + 1)
        self.state_size = s * (self.no_of_TT + 1) + Config.no_of_machines + 1
        
        self.state = None
        
        self.rewards = pd.DataFrame(columns=['completion_gain','energy_loss','defer','drop','wrong_task_selection',
        'full_machine_mapping','reward'])
        self.done = False
        self.res_val = 0 
        

        if isfile('./model.h5'):
            self.model = load_model('model.h5')
        else:
            self.model = self.nn_model()
        
        #self.model = load_model('model.h5')
        

        
        
    
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
        reward = -0.15 * pow(2, task.no_of_deferring)
        reward_detail = {'defer':reward}        
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

        return nxt_state, reward, reward_detail


    def drop(self, task):        
        task.status = TaskStatus.CANCELLED
        task.drop_time = Config.current_time
        self.stats['dropped'].append(task)
        self.unmapped_task = -1
        if task.urgency == UrgencyLevel.BESTEFFORT:
            reward = -0.2
        else:
            reward = -10
        
        reward_detail = {'drop':reward}
        
        
        nxt_state = self.encode_state()
        s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
            task.id, Config.current_time        )
        Config.log.write(s)
        #print(s)
        
        return nxt_state, reward, reward_detail


    def map(self, selected_task_index, machine):       
           
        gain, loss = machine.admit(self.unmapped_task)      
        
        if  gain == 'notEmpty' :                       
            self.insert(selected_task_index, self.unmapped_task)
            self.unmapped_task = -1
            nxt_state = self.encode_state()
            reward = -2.0
            reward_detail = {'full_machine_mapping':reward}
            
        else:
            reward = gain - loss            
            self.unmapped_task.assigned_machine = machine            
            self.stats['mapped'].append(self.unmapped_task)
            self.unmapped_task = -1                      
            nxt_state = self.encode_state()
            reward_detail = {'completion_gain':gain,
                    'energy_loss':loss }
        
        
        return nxt_state, reward, reward_detail


    def encode_state(self):
        state = []
        s = Config.batch_queue_size + Config.no_of_machines * (Config.queue_size + 1) 
        tasks_one_hot = np.zeros((s, self.no_of_TT+1))
        
        for task in reversed(self.batch_queue):
            if task != -1 :
                state.append(task.type.id)
            else:
                state.append(0)       
        
        
        for machine in Config.machines:            
            
            for task in reversed(machine.queue):
                if task != -1:
                    state.append(task.type.id)
                else:
                    state.append(0)

            running_task = machine.running_task[0]    
            if running_task != -1:
                state.append(running_task.type.id)                
            else:
                state.append(0)
        
        state = np.array(state)            
        tasks_one_hot [np.arange(s), state ] = 1
        
        state = tasks_one_hot.flatten()

        for machine in Config.machines:       
            running_task = machine.running_task[0]    
            if running_task != -1:                
                execution_time = running_task.execution_time[machine.type.name]
                progress = (Config.current_time - running_task.start_time) / execution_time
                state = np.append(state, progress)
            else:                
                state = np.append(state,-1)
            
        energy_level = Config.available_energy / Config.total_energy

        state = np.append(state, energy_level)     

        return state.tolist()


    def reset(self):
        for machine in Config.machines:
            machine.reset()
        
        self.state = self.encode_state()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

        if len(self.memory) > self.train_start:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
    
    def act(self):

        #state = self.encode_state()             
        if np.random.random() <= self.epsilon:                  
            action = random.randrange(self.action_size)
            
        else:
            state = np.array(self.encode_state())            
            state = state.reshape((1,self.state_size))                       
            action =  np.argmax(self.model.predict(state))
            
        
            
        return action

    def step(self, action):

        state = self.encode_state()        
                
        # Mapping
        if action < self.action_size- 2 * self.batch_queue_size:
            assigned_machine = action % Config.no_of_machines # starts with zero
            selected_task_index = action // Config.no_of_machines 
            selected_task = self.choose(selected_task_index)
            if selected_task != -1:
                nxt_state, reward, reward_detail= self.map(selected_task_index, Config.machines[assigned_machine])
            else:
                nxt_state = state
                reward = -2.0
                reward_detail = {'wrong_task_selection':reward}
                

        # Deferring
        elif action >= self.action_size- 2 * self.batch_queue_size and action < self.action_size-  self.batch_queue_size:
            
            selected_task_index = action - ( Config.no_of_machines * self.batch_queue_size)
            selected_task = self.choose(selected_task_index)
            if selected_task != -1:
                nxt_state, reward, reward_detail = self.defer(self.unmapped_task)
            else:
                nxt_state = state
                reward = -2.0
                reward_detail = {'wrong_task_selection':reward}
                
        # Dropping
        else: 
            #print("DROP")
            selected_task_index = action - ( (Config.no_of_machines + 1) * self.batch_queue_size )
            selected_task = self.choose(selected_task_index)
            if selected_task != -1:
                nxt_state, reward,reward_detail = self.drop(self.unmapped_task)
            else:
                nxt_state = state
                reward = -2.0
                reward_detail = {'wrong_task_selection':reward}
        
        reward_detail['reward'] = reward

        self.rewards = self.rewards.append(reward_detail, ignore_index=True)

    
                    
        #self.rewards.append(reward)
        
        if Config.available_energy > 0:            
            done = False
        else:
            done = True
        self.steps += 1 
        
        #Config.history_writer.writerow([action, reward])        
       
        return nxt_state, reward, done



    def replay(self):

            if len(self.memory) < self.train_start:
                return
            
            minibatch = random.sample(self.memory, min(len(self.memory), self.sample_size))

            state = np.zeros((self.sample_size, self.state_size))
            next_state = np.zeros((self.sample_size, self.state_size))
            action, reward, done = [], [], []

            for i in range(self.sample_size):
                state[i] = minibatch[i][0]
                action.append(minibatch[i][1])
                reward.append(minibatch[i][2])
                next_state[i] = minibatch[i][3]
                done.append(minibatch[i][4])

            # do batch prediction to save speed
            target = self.model.predict(state)
            target_next = self.model.predict(next_state)
            
            for i in range(self.sample_size):
                # correction on the Q value for the action used                
                if done[i]:
                    target[i][action[i]] = reward[i]
                else:                    
                    target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))

            # Train the Neural Network with batches           
            self.model.fit(state, target, batch_size=self.batch_size, epochs = 1, verbose=0)

##############################################

    def nn_model(self):

        
        init = initializers.HeUniform()

        model = Sequential()
        model.add(Dense(64, input_dim = self.state_size, activation='relu',kernel_initializer=init))
        model.add(Dense(64,  activation='relu',kernel_initializer=init))
        model.add(Dense(self.action_size,  activation='linear',kernel_initializer=init))
        model.compile(loss="mse", optimizer=RMSprop(lr=0.00001), metrics=["accuracy"])

        # X_input = Input(input_shape)
        # X = Dense(8, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform')(X_input)
        # X = Dense(32, activation="relu", kernel_initializer='he_uniform')(X) 
        # #X = Dense(8, activation="relu", kernel_initializer='he_uniform')(X)
        # X = Dense(self.action_size, activation="relu", kernel_initializer='he_uniform')(X)
        # model = Model(inputs = X_input, outputs = X)
        #model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])
            
        return model
    
    def schedule(self):

        # if self.choose() == -1:            
        #     return -1
        enable = False
        for task in self.batch_queue:
            if task != -1:
                enable = True
        
        if not enable: 
            return 
        
        
        if self.model == None  and isfile('./model.h5'):            
            self.model = load_model('model.h5')
        elif self.model == None and (not isfile('./model.h5')):            
            self.model = self.nn_model()
        
        state = self.encode_state()
        self.state = state       
        action = self.act()
        

        nxt_state, reward, done = self.step(action)  
        self.remember(state, action, reward, nxt_state, done)

        if self.train and self.steps % 100 == 0 :
            self.replay()
       

    


    



