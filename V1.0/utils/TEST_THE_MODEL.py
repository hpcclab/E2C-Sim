#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 11:07:52 2021

@author: c00424072
"""

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model


np.random.seed(3)
states = pd.read_csv('./states.csv')

model = load_model('./model.h5')

states = states.replace(-1,0)
states = states[['BQ-2', 'BQ-1', 'm1_slot1', 'm1_running_TT', 'm2_slot1',
                 'm2_running_TT', 
                 'm1_progress','m2_progress', 'energy_level']]

states.iloc[:,-3:] = np.random.rand(states.shape[0],3)



test_set = pd.DataFrame(data = np.zeros((states.shape[0],21)),columns=range(21))

test_set.iloc[:,-3:] = states.iloc[:,-3:]

for index, row in states.iterrows():
    
    #test_set.iloc[index, row] = 1
    state = row.values[:-3].astype(int)
    one_hot = np.zeros((6,3))
    one_hot[np.arange(6),state] = 1
    test_set.iloc[index, :-3] = one_hot.flatten()

test = test_set.values.reshape((test_set.shape[0],21))
    
y_hat = model.predict(test)
print(y_hat)
action = np.argmax(y_hat, axis=1)
print(action)

states['action'] = action

states.to_csv('state-acation-RLS.csv',index= False)

    
    




