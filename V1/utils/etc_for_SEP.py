#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:33:11 2022

@author: c00424072
"""

import pandas as pd
import numpy as np
import os


SEPs = np.linspace(4.25,50.5,41)
SEPs = [4.25]
max_e = 10
m = 4
n=3
seed = 7
for SEP in SEPs:
    
    if SEP < 5:
        max_e = 10
    elif SEP < 20:
        max_e = 50
    else:
        max_e = 100
    
    for etc_id in range(1,2):    
        seed += 7
        #np.random.seed(seed)
        s_m_avg = max_e / SEP
        s_m_prod = pow(s_m_avg , m*n)
        
        s_m = np.zeros((m,n))
        s_t = np.zeros((m,n))
        err = 1e-5* s_m_prod
        f = 1
        while abs(np.prod(s_m) - s_m_prod ) > err:   
            for i in range(m):
                for j in range(n-1):
                    
                    if s_m_prod > f*100:            
                        s_m[i,j] =  np.random.uniform(1,f*100)
                        if (s_m_prod / s_m[i,j]) < 1:
                            s_m[i,j] = 1
                    
                    elif s_m_prod > 1.01:
                        s_m[i,j] =  np.random.uniform(1,s_m_prod)
                    
                    else:
                        
                        s_m[i,j] = s_m_prod
                    s_m_prod /= s_m[i,j]
                s_m[i][n-1] = 1.0
            s_m_prod = pow(s_m_avg , m*n)
            f +=1
        
        f = 1.0
        S_T_AVG = 1.0
        S_M_AVG = 0.0 
        e_in = np.random.uniform(0.5, f*max_e,m)
        iter = 0
        while S_T_AVG > S_M_AVG and iter<10:  
            print(S_M_AVG, S_T_AVG)      
            min_e_mj = np.min(e_in)
            argmin_in = np.argmin(e_in)
            e_in[-1], e_in[argmin_in] = e_in[argmin_in] , e_in[-1]
            
                
            # # e_mj = np.random.uniform(0.1, min_e_mj, n)
            # # e_mj[-1] = e_in[-1]        
            
            
            # e_inner = np.random.uniform(0.5, max_e, (m-1,n-1))
            # e_mj = np.zeros((1,n))
            # e_in = np.zeros((m,1))
            # for j in range(n-1):
            #     e_mj[0,j] = np.random.uniform(np.max(e_inner[:,j]), max_e)
            # for i in range(m-1):
            #     e_in[i,0] = np.random.uniform(np.max(e_mj), max_e)
            # e_in[-1,0] = np.random.uniform(np.max(e_mj), np.min(e_in[:-1,0]))
            # e_mj[0,-1] = e_in[-1,0]
            
            # for j in range(n):
            #     rnd = np.random.randint(0,m-2)
            #     s_m[rnd,j] = s_m[rnd,j]*s_m[m-1,j]/(e_mj[0,-1] / e_mj[0,j])
            #     s_m[m-1,j] = e_mj[0,-1] / e_mj[0,j]   
                
            
            etc = np.zeros((m,n))
            for i in range(m):
                for j in range(n):
                    if j < n-1:
                        etc[i,j] = e_in[i] / s_m[i,j]
                    etc[i,n-1] = e_in[i] 
            
            df = pd.DataFrame(etc, columns = [f'M{i}' for i in range(n)],
                                index = [f'{i}' for i in range(m)])        
            S_T = df.max(axis=0) / df
            S_M = df.divide(df.max(axis=1), axis=0)
            S_M = 1 / S_M
            S_T_AVG = pow(S_T.product().product(), 1/(m*n))
            S_M_AVG = pow(S_M.product().product(), 1/(m*n))
            
            i_max = int(S_T.idxmax()[S_T.max().idxmax()])
            j_max = S_T.columns.get_loc(S_T.max().idxmax())

            e_in[i_max] *= f
            f *= 0.95
            iter +=1
            
            
        path = f"../tasK_machine_performance/heterogeneous/{str(SEP).split('.')[0]}_{str(SEP).split('.')[1]}"
        os.makedirs(path, exist_ok = True)
        df.to_csv(f'{path}/etc-{etc_id}.csv', index=False)
        print(f'SEP: {SEP}  etc_id: {etc_id} S_M: {S_M_AVG}, S_T: {S_T_AVG}')

