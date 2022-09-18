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

SEPs = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0 ,13.0, 14.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0,55.0 ,60.0,65.0, 70.0, 75.0,80.0,81.0,82.0,83.0,84.0, 85.0, 86.0, 87.0,88.0,89.0,90.0, 100.0, 110.0 ]
#SEPs= [4.0]
max_es = [1.0, 2.0, 10.0, 50.0, 150]
max_beta = 20
max_param = 100

m = 4
n=4

seed = 7 
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
        
    a = (SEP/(2*max_e))
    b = (SEP/(2*max_e))
    c = -1
    
    delta = b*b - 4*a*c
    x1 = (1/(2*a))*(-b - np.sqrt(delta))
    x2 = (1/(2*a))*(-b + np.sqrt(delta))
    

    for etc_id in range(30):
        seed = 7*(etc_id)
        np.random.seed(seed)
        
        epsilon = np.ones(n)
        if x1<=0 :
            x1 = 1
        assert x2 <= np.sqrt(2*max_e/SEP)
        beta = np.random.uniform(x1, x2, m)
        beta[m-1] = 1
        beta = np.sort(beta)[::-1] 
        beta_inv = [1/x for x in beta]

        sum_beta = np.sum(beta)
        sum_beta_inv = np.sum(beta_inv)
        
        param = ((2*max_e / SEP) - (sum_beta/sum_beta_inv))*(n/m)*sum_beta_inv        
        assert param>n        
        param -=1         
        for j in range(n-2):
            if param > max_param:
                epsilon[j] = np.random.uniform(1, max_param)
            else:
                epsilon[j] = np.random.uniform(1,param)
            if param - epsilon[j] < n-(j+1):
                epsilon[j] = 1
            param -= epsilon[j]
        epsilon[n-2] = param if param>1 else 1
        epsilon = np.sort(epsilon)[::-1]
                
        etc = np.ones((m,n))
        
        for i in range(m):
            for j in range(n):
                etc[i,j] = round(max_e / (beta[i]* epsilon[j]),4)
        
        
        df = pd.DataFrame(etc, columns = [f'm{j+1}' for j in range(n)],
                            index = [f'T{i}' for i in range(m)])        
        S_T = df.max(axis=0) / df
        S_M = df.divide(df.max(axis=1), axis=0)
        S_M = 1 / S_M
        S_T_AVG =  S_T.mean().mean()
        S_M_AVG =  S_M.mean().mean()
        S_AVG = 0.5*(S_T_AVG + S_M_AVG )
        SEP_new = df.iloc[:,-1].mean() / S_AVG
        assert abs(SEP_new - SEP) <0.02

        SEP_str = f'{int(SEP)}_{(str(SEP-int(SEP))).split(".")[1]}'
                    
        path = f"../task_machine_performance/heterogeneous_arithmetic/{SEP_str}"
        os.makedirs(path, exist_ok = True)
        df.to_csv(f'{path}/etc-{etc_id}.csv', index=False)
        print(f'SEP_target: {SEP}  SEP_calc:{SEP_new} etc_id: {etc_id} S_M: {S_M_AVG}, S_T: {S_T_AVG}')




