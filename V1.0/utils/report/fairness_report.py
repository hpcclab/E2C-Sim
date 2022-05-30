
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


schedulers = ['FEE','EE','MM','MMU','MSD']
task_types = ['TT1','TT2','TT3','TT4']
#task_types = ['TT1','TT2']
workload = '3-0'


def read_results(workload,scheduler,sample):
    global task_types
    
    path = f'../../output/data/{workload}//{scheduler}/detailed-{sample}.csv'    
    detailed = pd.read_csv(path, usecols=['type','status'])    
    task_types = detailed['type'].unique()
    
    return detailed


def completion_rates(detailed):
    global task_types
    columns = np.append(task_types,['total'])
    result = pd.DataFrame(columns=columns)
    
    total_arrived = 0
    total_completed = 0
    
    for tt in task_types:
        
        arrived = detailed.loc[detailed['type']==tt].shape[0]
        completed = detailed.loc[(detailed['type']==tt)  
                                 &
                                 (
                                     (detailed['status'] == 'COMPLETED')
                                     | 
                                     (detailed['status'] == 'XCOMPLETED'))].shape[0]
        total_arrived += arrived
        total_completed += completed
        
        if arrived != 0 :
            completion_rate =  completed / arrived
        else:
            completion_rate = 0        
       
        result[tt] = [100*completion_rate]
    if total_arrived != 0:
        result['total'] = 100 * total_completed / total_arrived
    else:
        result['total'] = 0.0
        
        
    return result.round(2)

def average_cr(workload, scheduler):
    for i in range(30):               
        detailed = read_results(workload,scheduler,i)
        if i == 0:
            results = pd.DataFrame(columns=task_types)
            
        result = completion_rates(detailed)    
        results = results.append(result, ignore_index=True)
    
    return results.mean()



count = 0
for scheduler in schedulers:    
    result = average_cr(workload, scheduler)
    
    if count == 0:
        results = pd.DataFrame(columns=np.append(task_types,['total']), index = schedulers)
    #print(results)
    results.loc[scheduler,:] = result
    
    count += 1
print(results)
results = results.rename(index={'EE':'ELARE', 'FEE':'FELARE'})


hatch = ['\\\\\\','///','...','xxx']
#hatch = ['..','xx']
colors = ['navy','darkred','green', 'orange']

fig, ax1 = plt.subplots()
#plt.title('Example of Two Y labels')
ax2 = ax1.twinx()
width = 0.5
dist = 1.0
schedulers_label  = ['FELARE','ELARE','MM','MMU','MSD']
r0 = 0
r = [(r0-1.5*width+i*(4*width+dist)) for i in range(len(schedulers))]
print(r)
i = 0
 

for i in range(len(task_types)):
    
    tt = task_types[i]
    r = [r[k] + width for k in range(len(r))]
    
    print(i, tt, r)
    ax1.bar(r, results[tt].values, label = tt, color='none',zorder=0,
            hatch = hatch[i],edgecolor=colors[i], width=width)
    
    ax1.bar(r, results[tt].values,color='none',zorder=1,
            edgecolor='k', width=width)
    
    #i +=1
    


r = [r[k] - 1.5*width for k in range(len(r))]    
ax2.plot(r, results['total'], '--',marker = 's',color = 'red', label = 'collective')       
       


plt.xticks(r,schedulers_label )



#ax2.set_ylabel(r'$\frac{\mathrm{\# completed\ tasks}}{\mathrm{\# total\ tasks} }$', fontsize = 14)
ax2.set_ylabel('collective completion rate', fontsize = 14)
ax2.tick_params(axis='y', which='major', labelsize=14)
ax2.set_ylim([0,60])

ax1.set_ylim([0,60])
ax1.set_xlabel('heuristics', fontsize = 14)
#ax1.set_ylabel(r'$\frac{\mathrm{\# completed\ task-type}}{\mathrm{\# total\ arrived\ task-type} }$', fontsize = 14)
ax1.set_ylabel('task type completion rate', fontsize = 14)
ax1.tick_params(axis='both', which='major', labelsize=14)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

lines = lines_1 + lines_2
labels = labels_1 + labels_2

ax1.legend(lines, labels, loc=0)

#plt.grid(axis='y')
# ax1.legend()
# ax2.legend(loc=[0.85,0.5])

plt.tight_layout()

#plt.grid(linestyle='dotted')
#plt.savefig(f'../../output/figures/fairness-phases-{workload}-more-heuristics-real.pdf',dpi=300)
plt.show()      
    
    
    
    