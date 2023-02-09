#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:33:11 2022

@author: c00424072
"""
import pandas as pd
import numpy as np
import os

#np.random.seed(10) 

SEPs = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0 ,13.0, 14.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 75.0, 100.0 ]
SEPs= [4.0]
max_es = [1.0, 2.0, 10.0, 50.0, 150]
max_param = 100
m = 4
n=4

seed = 7 
log = open('log.txt','w')
for SEP in SEPs: 
    if SEP <= 0.5:
        max_e = max_es[0]
    elif SEP <= 1.0:
        max_e = max_es[1]
    elif SEP <= 5.0:
        max_e = max_es[2] 
    elif SEP < 20.0:
        max_e = max_es[3]
    else:
        max_e = max_es[4]

    for etc_id in range(30):
        log.write(f'************ etc:{etc_id} **********')
        
        seed = 7*(etc_id)
        np.random.seed(seed)
        
        epsilon = np.ones(n)
        beta = np.ones(m)
        
        param = max_e / SEP        
        param_beta = pow(param,m)
        param_epsilon = pow(param,n)
        
       
        print(param_beta, param_epsilon)
        for i in range(m-2):
            print(f'** {i} **', param_beta, beta)
            if param_beta > max_param and i<2:
                beta[i]= np.random.uniform(1, max_param)
            else:
                beta[i] = np.random.uniform(1, param_beta)
            
            param_beta /= beta[i]
        beta[m-2] = param_beta
        
        
        for j in range(n-2):
            if param_epsilon > max_param and j<2:
                epsilon[j] = np.random.uniform(1, max_param)
            else:
                epsilon[j] = np.random.uniform(1, param_epsilon)
            
            param_epsilon /= epsilon[j]
        epsilon[n-2] = param_epsilon
        
        
        beta = np.sort(beta)[::-1]        
        epsilon = np.sort(epsilon)[::-1]
        
        assert abs(np.product(beta) - pow(param,m)) <1e-3
        assert abs(np.product(epsilon) - pow(param,n)) < 1e-3
        
        
        etc = np.ones((m,n))
        
        for i in range(m):
            for j in range(n):
                etc[i,j] = round(max_e / (beta[i]* epsilon[j]),4)
        
        
        df = pd.DataFrame(etc, columns = [f'm{j+1}' for j in range(n)],
                            index = [f'T{i}' for i in range(m)])        
        S_T = df.max(axis=0) / df
        S_M = df.divide(df.max(axis=1), axis=0)
        S_M = 1 / S_M
        S_T_AVG = pow(S_T.product().product(), 1/(m*n))
        S_M_AVG = pow(S_M.product().product(), 1/(m*n))
        S_AVG = np.sqrt(S_M_AVG*S_T_AVG)
        SEP_new = max_e / S_AVG
        
    
        
        SEP_str = f'{int(SEP)}_{(str(SEP-int(SEP))).split(".")[1]}'
                    
        path = f"../task_machine_performance/heterogeneous/{SEP_str}"
        os.makedirs(path, exist_ok = True)
        #df.to_csv(f'{path}/etc-{etc_id}.csv', index=False)
        print(f'SEP: {SEP}  etc_id: {etc_id} S_M: {S_M_AVG}, S_T: {S_T_AVG}')




