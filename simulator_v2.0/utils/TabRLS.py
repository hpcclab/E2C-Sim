import heapq
from Event import Event, EventTypes
from BaseTask import TaskStatus, UrgencyLevel
from BaseScheduler import BaseScheduler
import Config
from Task import Task


import numpy as np
import random
from collections import deque 
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam, RMSprop
from math import ceil
from os.path import isfile
from enum import Enum, unique

@unique
class Actions(Enum):
    DEFER = 0
    MAP_TO_CPU = 1
    MAP_TO_GPU = 2
    DROP = 3
    OFFLOAD = 4


class RLS(BaseScheduler):
    
    machine_index = 0

    def __init__(self, total_no_of_tasks):
        super().__init__()

        self.total_no_of_tasks = total_no_of_tasks
        #self.EPISODES = 30
        self.memory = deque(maxlen=1800)

        self.gamma = 0.9  # discount rate
        #self.epsilon = 0.85  # exploration rate
        self.epsilon = 0.0  # exploration rate
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.9
        self.batch_size = 32
        self.train_start = 32

        self.steps = 0
        self.model = load_model('model.h5')
        #self.model = None

        self.action_size = Config.no_of_machines + 3
        self.state_size = Config.no_of_machines *(Config.queue_size + 1) +1
        self.state = [-1] * self.state_size
        self.done = False
        
    
    def feed(self):

        while (self.unlimited_queue and (-1 in self.batch_queue)):
            task = self.unlimited_queue.pop(0)
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task


    def choose(self):
        index = 0        
        if self.batch_queue[index] != -1:
            self.unmapped_task = self.batch_queue[index]
            self.batch_queue = self.batch_queue[:index] + self.batch_queue[index+1:]+[-1]            
            self.feed()
            return self.unmapped_task
                         
        else:            
            self.unmapped_task = -1
            return -1
    

    def offload(self, task):
        reward = Config.cloud.admit(task)
        self.stats['offloaded'].append(task)
        nxt_state = self.get_state()
            
        return nxt_state, reward

    
    def defer(self,task):
        if task.urgency == UrgencyLevel.BESTEFFORT:
            if Config.current_time > task.deadline + task.devaluation_window:
                nxt_state, reward = self.drop(task)
                return nxt_state, reward
        elif task.urgency == UrgencyLevel.URGENT:
            if Config.current_time > task.deadline:
                nxt_state, reward = self.drop(task)
                return nxt_state, reward
        
        if -1 in self.batch_queue:
            empty_slot = self.batch_queue.index(-1)
            self.batch_queue[empty_slot] = task
        else:
            replaced_task = self.batch_queue[-1]
            self.unlimited_queue = [replaced_task] + self.unlimited_queue
            self.batch_queue[-1] = task
        task.status =  TaskStatus.DEFERRED
        self.stats['deferred'].append(task)
        reward = -0.05     
        nxt_state = self.get_state()
        
        # last_event = heapq.nlargest(1, Config.event_queue.event_list)[0]
        # event_time = last_event.time
        # event = Event(event_time, EventTypes.DEFERRED, task)
        # Config.event_queue.add_event(event)
        s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
           task.id, Config.current_time        )
        Config.log.write(s)
        #print(s)

        return nxt_state, reward


    def drop(self, task):        
        task.status = TaskStatus.CANCELLED
        task.drop_time = Config.current_time
        self.stats['dropped'].append(task)

        if task.urgency == UrgencyLevel.BESTEFFORT:
            reward = -0.1
        else:
            reward = -0.5
        
        nxt_state = self.get_state()
        s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
            task.id, Config.current_time        )
        Config.log.write(s)
        #print(s)
        
        return nxt_state, reward

    def map(self, machine):
        
        reward = machine.admit(self.unmapped_task)
       
        if  reward == 'notEmpty' :
            #print("WARNING: machine "+ str(machine.id) +
            #" cannot admit Task "+ str(self.unmapped_task.id))
            nxt_state, _ = self.defer(self.unmapped_task)
            reward = -20            
            
        else:            
            self.unmapped_task.assigned_machine = machine            
            self.stats['mapped'].append(self.unmapped_task)            
            nxt_state = self.get_state()
            

        return nxt_state, reward
    

    def nn_model(self):
        input_shape = (self.state_size,)

        X_input = Input(input_shape)
        X = Dense(128, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform')(X_input)
        X = Dense(64, activation="relu", kernel_initializer='he_uniform')(X) 
        X = Dense(32, activation="relu", kernel_initializer='he_uniform')(X)
        X = Dense(self.action_size, activation="linear", kernel_initializer='he_uniform')(X)
        model = Model(inputs = X_input, outputs = X)
        model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])
            
        return model

    
    def get_state(self):
        machine_queues = []
        running_tasks = []
        for machine in Config.machines:
            queue = np.array(machine.queue)
            machine_queues.append(queue)
            running_tasks.append(machine.running_task)
        
        machine_queues = np.array(machine_queues)
        running_tasks = np.array(running_tasks)

        if self.unmapped_task != -1:
            state = [self.unmapped_task.type.id]
        else:
            state = [-1]

        for machine_queue in machine_queues:
            for task in machine_queue:
                if task != -1:
                    state.append(task.type.id)
                else:
                    state.append(-1)
        
        for running_task in running_tasks:
            if running_task != -1:
                state.append(running_task[0].type.id)
            else:
                state.append(-1)
                
        return state
    
    def reset(self):
        for machine in Config.machines:
            machine.reset()
        
        self.state = self.get_state()


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.train_start:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay


    def act(self):
            
        if np.random.random() <= self.epsilon:
        #if np.random.random() <= 0.0:
            #print('RANDOM ACTION:')
            action = random.randrange(self.action_size)
        else:
            #print('GREEDY:')
            input_state = np.array(self.state)
            input_state = input_state.reshape((1,self.state_size))
            action =  np.argmax(self.model.predict(input_state))

        return action

    def step(self, action):
       
        if action == 0 :
            #print('defer -->>')
            nxt_state, reward = self.defer(self.unmapped_task)
        elif action in list(range(1, Config.no_of_machines +1 )):
            #print('map -->> {}'.format(action))
            nxt_state, reward = self.map(Config.machines[action-1])
        elif action == Config.no_of_machines +1:
            #print('Cancel -->>')
            nxt_state, reward = self.drop(self.unmapped_task)
        elif action == Config.no_of_machines +2:
            #print('offload -->>')
            nxt_state, reward = self.offload(self.unmapped_task)

        #if self.steps < self.total_no_of_tasks and Config.available_energy > 0:
        if Config.available_energy > 0:
            self.steps +=1 
            done = False
        else:
            done = True
        # self.steps += 1 
        # done = False
        s = '\nAction: {}  Reward: {} '. format(action, reward)
        #print(s)
        Config.history_writer.writerow([action, reward])
        return nxt_state, reward, done

    
    def replay(self):

            if len(self.memory) < self.train_start:
                return
            # Randomly sample minibatch from the memory
            #print('********** REPLAY **********************')
            minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))

            state = np.zeros((self.batch_size, self.state_size))
            next_state = np.zeros((self.batch_size, self.state_size))
            action, reward, done = [], [], []

            for i in range(self.batch_size):
                state[i] = minibatch[i][0]
                action.append(minibatch[i][1])
                reward.append(minibatch[i][2])
                next_state[i] = minibatch[i][3]
                done.append(minibatch[i][4])

            # do batch prediction to save speed
            target = self.model.predict(state)
            target_next = self.model.predict(next_state)
            
            for i in range(self.batch_size):
                # correction on the Q value for the action used
                
                if done[i]:
                    target[i][action[i]] = reward[i]
                else:                    
                    target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))

            # Train the Neural Network with batches
            #print(25 * '*' + 'TRAINING ' + 25 * '*' )
            self.model.fit(state, target, batch_size=self.batch_size, epochs = 5, verbose=0)



     
    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)

    
    def schedule(self):

        if self.choose() == -1:            
            return -1

        state = self.get_state()
        if self.model == None  and isfile('./model.h5'):
            self.load('model.h5')
        elif self.model == None and (not isfile('./model.h5')):
            self.model = self.nn_model()
        action = self.act()        
        next_state, reward, done = self.step(action)
        self.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            self.save("model.h5")
            return
        if self.steps%50 == 0:
            self.replay()

    # def schedule(self):

    #     if self.choose() == -1:            
    #         return -1
        
        
    #     action = self.act()        
    #     self.step(action) 

            


