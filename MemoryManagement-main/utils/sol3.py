"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Jan, 18, 2022
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt

import utils.config as config
from utils.application import Application, AppStatus
from utils.event import Event, EventTypes



class Simulator:

    def __init__(self):                             
        self.stats = {'missed':0,}
        
    def read_workload(self, workload_id):
        path_to_workload = f'{config.path_to_workloads}/workload-{workload_id}.csv'
        workload = pd.read_csv(path_to_workload)
        return workload 
    
    def initialize(self, workload_id):
        workload = self.read_workload(workload_id)        
        for _, request in workload.iterrows():  
            app_name = request[0]
            request_time = request[1]          
            app = config.find_app(app_name)
            event_time = request_time - config.window
            event = Event(event_time, EventTypes.STARTED, app)
            config.event_queue.add_event(event)

    
    def run(self):
        while config.event_queue.event_list:
            event = config.event_queue.get_first_event()
            app = event.event_details
            config.time.set_time(event.time)
            s = f'\nEvent: {event.event_type.name} @{event.time:3.1f}'
            s += f'  ==>> {app.name} Free Memory:{config.memory.free}'                       
            config.log.write(s)
            if event.event_type == EventTypes.STARTED:
                if app.status != AppStatus.AGGRESSIVE:                         
                    self.allocate(app)
                else:
                    for e in config.event_queue.event_list:
                        if e.event_type == EventTypes.FINISHED and e.event_details.name == app.name:
                            config.event_queue.remove(e)
                            app.finish_time = config.time.get_time() + 2 * config.window
                            app.stats['finish_times'][-1] = app.finish_time
                            new_event = Event(app.finish_time, EventTypes.FINISHED, app)
                            config.event_queue.add_event(new_event)
                            break

            elif event.event_type == EventTypes.FINISHED:
                app.status = AppStatus.MINIMAL                
        
            
         

    def allocate(self, app):
        allocated = False  
        for best_model_size in reversed(app.models):

            if best_model_size == app.loaded_model_size:
                app.status = AppStatus.AGGRESSIVE
                app.start_time = config.time.get_time()             
                app.finish_time = config.time.get_time() + 2*config.window 
                event = Event(app.finish_time, EventTypes.FINISHED, app)
                config.event_queue.add_event(event)
                allocated = True
                #print(f'{app.name} @{time} : best model is there')
                break
                                                
            else:
                config.memory.release(app.loaded_model_size)
                app.loaded_model_size = 0.0
                #print(f'{app.name} @{time} : no model')

            if best_model_size <= config.memory.free :
                config.memory.allocate(best_model_size)
                app.status = AppStatus.AGGRESSIVE
                app.loaded_model_size = best_model_size
                app.finish_time = config.time.get_time() + 2*config.window 
                event = Event(app.finish_time, EventTypes.FINISHED, app)
                config.event_queue.add_event(event)
                allocated = True                
                break      

            else:
                is_enough_space, candids = self.provisionally_evict(best_model_size)
                if is_enough_space:
                    for candid in candids:                        
                        self.evict(candid[0], candid[1])                        
                            
                    config.memory.allocate(best_model_size)
                    app.status = AppStatus.AGGRESSIVE
                    app.start_time = config.time.get_time()             
                    app.finish_time = config.time.get_time() + 2*config.window 
                    app.loaded_model_size = best_model_size
                    event = Event(app.finish_time, EventTypes.FINISHED, app)
                    config.event_queue.add_event(event)
                    allocated = True
                    
                    break
           
        app.stats['requested_times'].append(config.time.get_time())
        app.stats['finish_times'].append(app.finish_time)        
        app.stats['evicted_times'].append(None)
        app.stats['allocated_memory'].append(app.loaded_model_size)

        app.timeseries['time'].append(config.time.get_time())
        app.timeseries['allocated_memory'].append(app.loaded_model_size)
        
        if not allocated: 
            self.stats['missed'] += 1
            s = f'\n{app.name} cancelled'
        else:
            s = f'\nA model of size {best_model_size} was allocated to {app.name}'
        config.log.write(s)
                
    def evict(self, candid, reload=False):
        if reload:        
            config.memory.release(candid.loaded_model_size - candid.models[0])
            candid.loaded_model_size = candid.models[0]
        else:
            config.memory.release(candid.loaded_model_size)
            candid.loaded_model_size = 0.0 
        candid.status = AppStatus.MINIMAL
        candid.evict_time = config.time.get_time()

        candid.stats['requested_times'].append(None)
        candid.stats['finish_times'].append(None)
        candid.stats['evicted_times'].append(candid.evict_time)
        candid.stats['allocated_memory'].append(candid.loaded_model_size)

        candid.timeseries['time'].append(config.time.get_time())
        candid.timeseries['allocated_memory'].append(candid.loaded_model_size)

        s = f'\n {candid.name} EVICTED @{config.time.get_time()}'
        if reload:
            s+= f' and RELOADED with {candid.loaded_model_size}'
        config.log.write(s)


    def candidates(self):
        candids = []
        for app in  config.apps:
            if app.status != AppStatus.AGGRESSIVE and app.loaded_model_size > 0.0:
                candids.append(app)
        return candids    

    def pick(self,candids, required_memory):
        
        try:
            if config.eviction_method =='first_fit':
                picked, candids = self.first_fit(candids)
                reload = False
            elif config.eviction_method =='best_fit':
                picked, candids, reload = self.best_fit(candids, required_memory)
            else:
                raise Exception(f'ERROR[simulator.py --> pick()]:The {config.eviction_method} as eviction method has not defined!')
        except Exception as err:
            print(err)
            sys.exit()
        
        return picked, candids, reload
      
    
    def provisionally_evict(self, required_memory):                      
        candids = self.candidates()
        s=f'\n ******** Provisionally Evict ({required_memory})************'
        s+='\nCandids:\n[ '
        for candid in candids:
            s += f'  [{candid.name}, {candid.loaded_model_size}]  ' 
        s+=' ]'       
        config.log.write(s)

        picked =[]
        
        count = 0
        while candids and required_memory > 0:            
            s =f'\ncurrent required memory[{count}]: {required_memory}'                        
            candid, candids, reload = self.pick(candids, required_memory)
            picked.append([candid, reload])            
            required_memory -= candid.loaded_model_size
            s += f'\nnew required memory: {required_memory}'
            s+='\nCandids:\n[ '            
            for candid in candids:
                s += f'  [{candid.name}, {candid.loaded_model_size}]  ' 
            s+=' ]'       
            config.log.write(s)                       
            count +=1 
        is_enough_space = bool(required_memory<=0)

        s ='\nPicked:\n[ '
        for candid in picked:
            c = candid[0]
            s += f'  [{c.name}, {c.loaded_model_size}]  '
        s+=' ]'       
        config.log.write(s)

        return is_enough_space, picked
    
    def get_2nd_element(self,candid_difference):
        return candid_difference[1]

    def first_fit(self, candids):
        candids.sort(reverse=True)
        picked = candids[0]
        candids.remove(picked)
        return picked, candids
        
    
    def best_fit(self, candids, required_memory):
        remainders = []
        needed = []
        for candid in candids:
            difference = candid.loaded_model_size - required_memory
            if difference >= 0:
                remainders.append([candid, difference])
            else:
                needed.append([candid, difference])           
        
        reload = False
        if remainders:            
            remainders.sort(key= self.get_2nd_element) 
            for remainder in remainders:
                if remainder[1] >= candid.models[0]:
                    picked = remainder[0]
                    reload = True
                else:
                    picked = remainders[0][0]            
        else:
            needed.sort(key= self.get_2nd_element, reverse=True)            
            picked = needed[0][0]
              
        candids.remove(picked)
        return picked, candids, reload
    
    def report(self):
        df_report = pd.DataFrame(columns = ['app','requested_times','finish_times',
        'evicted_times','allocated_memory','best_model'])
        
        for app in config.apps:
            
            df = pd.DataFrame(app.stats)            
            df['app'] = app.name
            df['best_model'] = app.models[-1]
            df_report = df_report.append(df, ignore_index=True)
        
        
        max_request_time = df_report['requested_times'].max()
        for app in config.apps:
            app.stats['requested_times'].insert(0,0.0)
            app.stats['allocated_memory'].insert(0,0.0)

            app.stats['requested_times'].append(max_request_time)
            app.stats['allocated_memory'].append(app.loaded_model_size)


        df_report = df_report.sort_values(by=['requested_times'])
        df_report = df_report.reset_index(drop=True)               
        df_report.to_csv('./output/report.csv', index =False)
    
    def plot_mem_usage(self, apps):
        plt.figure(figsize=(16,4)) 
        markers = ['o','x','<','>','+'] 
        count = 0      
        for app in config.apps:            
            if app.name in apps:                 
                plt.step(app.timeseries['time'], app.timeseries['allocated_memory'],
                 marker= markers[count], markersize = 10,
                 linestyle='-',
                 where='post',label = app.name)
            count+=1
            count = count%(len(markers))

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Memory Usage')            
        plt.savefig('./output/figures/mem_usage.pdf',dpi=300)
        plt.show()
