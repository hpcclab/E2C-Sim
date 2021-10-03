import Config
from RLS import RLS

import numpy as np
import random
from collections import deque 
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam, RMSprop

class RLSAgent:


    def __init__(self):
        # machine_queues = []
        # running_tasks = []
        # for machine in Config.machines:
        #     queue = np.array(machine.queue)
        #     machine_queues.append(queue)
        #     running_tasks.append(machine.running_task)
        
        # machine_queues = np.array(machine_queues)
        # running_tasks = np.array(running_tasks)

        # self.state = [self.unmapped_task]
        # for machine_queue in machine_queues:
        #     self.state += machine_queue
        
        # for running_task in running_tasks:
        #     self.state += running_task               
        self.total_no_of_tasks = 10
        self.EPISODES = 1000
        self.memory = deque(maxlen=2000)

        self.gamma = 0.95    # discount rate
        self.epsilon = 0.01  # exploration rate
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.999
        self.batch_size = 64
        self.train_start = 100

        self.steps = 0
        self.model = None

        self.action_size = Config.no_of_machines + 2
        self.state_size = Config.no_of_machines *(Config.queue_size + 1) +1
        self.state = [-1] * self.state_size


    def nn_model(self):
        input_shape = (self.state_size,)

        X_input = Input(input_shape)
        X = Dense(64, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform')(X_input)
        X = Dense(32, activation="relu", kernel_initializer='he_uniform')(X) 
        X = Dense(16, activation="relu", kernel_initializer='he_uniform')(X)
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
            action = random.randrange(self.action_size)
        else:
            input_state = np.array(self.state)
            input_state = input_state.reshape((1,self.state_size))
            action =  np.argmax(self.model.predict(input_state))

        return action

    def step(self, action):
        print('action = '+str(action))
        if self.unmapped_task != -1:
            print('unmapped_task: '+ str(self.unmapped_task.id))        
        
        if action == 0 :
            nxt_state, reward = RLS.defer(self.unmapped_task)
        elif action in list(range(1, Config.no_of_machines +1 )):
            nxt_state, reward = RLS.map(Config.machines[action-1])
        elif action == Config.no_of_machines +1:
            nxt_state, reward = RLS.drop()

        if self.steps < self.total_no_of_tasks:
            self.steps +=1 
            done = False
        else:
            done = True

        return nxt_state, reward, done

    
    def replay(self):
            if len(self.memory) < self.train_start:
                return
            # Randomly sample minibatch from the memory
            minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))

            state = np.zeros((self.batch_size, self.state_size))
            next_state = np.zeros((self.batch_size, self.state_size))
            action, reward, done = [], [], []

            # do this before prediction
            # for speedup, this could be done on the tensor level
            # but easier to understand using a loop
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
                    # Standard - DQN
                    # DQN chooses the max Q value among next actions
                    # selection and evaluation of action is on the target Q Network
                    # Q_max = max_a' Q_target(s', a')
                    target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))

            # Train the Neural Network with batches
            print(25 * '*' + 'TRAINING ' + 25 * '*' )
            self.model.fit(state, target, batch_size=self.batch_size, verbose=0)

     
    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)

    
    def train(self):

        if self.choose() == -1:
            return
        state = self.get_state()

        if self.model == None:       
            self.nn_model()
        action = self.act()
        next_state, reward, done = self.step(action)                              
        self.remember(state, action, reward, next_state, done)
        state = next_state
        self.replay()


    def schedule(self):
        if self.choose() == -1:
            return
        state = self.get_state()

        if self.model == None:       
            self.nn_model()
        
        input_state = np.array(self.state)
        input_state = input_state.reshape((1,self.state_size))
        action =  np.argmax(self.model.predict(input_state))
        self.step(action)      
                       
        
