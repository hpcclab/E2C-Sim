
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


schedulers = ['FEE*']
scheduler = 'FEE*'
task_types = ['TT1','TT2']
workload = '3-3'
fairness_factors = [0,2,4,6,8,10]


def read_results(workload,scheduler,fairness_factor,sample):
    global task_types
    
    path = f'../../output/data/{workload}/{scheduler}-F{fairness_factor}/detailed-{sample}.csv'    
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

def average_cr(workload, scheduler, fairness_factor):
    for i in range(30):               
        detailed = read_results(workload,scheduler,fairness_factor,i)
        if i == 0:
            results = pd.DataFrame(columns=task_types)
            
        result = completion_rates(detailed)    
        results = results.append(result, ignore_index=True)
    
    return results.mean()



count = 0
for fairness_factor in fairness_factors:
    
    result = average_cr(workload, scheduler,fairness_factor)
    if count == 0:
        results = pd.DataFrame(columns=np.append(task_types,['total']), index = fairness_factors)
    #print(results)
    results.loc[fairness_factor,:] = result
    
    count += 1
print(results)



hatch = ['\\\\\\','///']
colors = ['navy','darkred']

fig, ax1 = plt.subplots()
#plt.title('Example of Two Y labels')
ax2 = ax1.twinx()
width = 0.5
dist = 1.0
schedulers_label  = schedulers
r0 = 0
r = [(r0-0.5*width+i*(2*width+dist)) for i in range(len(fairness_factors))]
i = 0
 
for tt in task_types:
    
    r = [r[k] + i*width for k in range(len(r))]
    print(r)
    ax1.bar(r, results[tt].values, label = tt,color='none',zorder=0,
            hatch = hatch[i],edgecolor=colors[i], width=width)
    
    ax1.bar(r, results[tt].values, color='none',zorder=1,
            edgecolor='k', width=width)
    
    i +=1
    


r = [r[k] - 0.5*width for k in range(len(r))]    
ax2.plot(r, results['total'], '--',marker = 's',color = 'red', label = 'total')       
       

xlabels = [f/10 for f in fairness_factors ]
plt.xticks(r,xlabels )



ax2.set_ylabel(r'$\frac{\mathrm{\# completed\ tasks}}{\mathrm{\# total\ tasks} }$', fontsize = 14)
ax2.tick_params(axis='y', which='major', labelsize=14)
ax2.set_ylim([0,95])

ax1.set_ylim([0,95])
ax1.set_xlabel('fairness factor', fontsize = 14)
ax1.set_ylabel(r'$\frac{\mathrm{\# completed\ task-type}}{\mathrm{\# total\ arrived\ task-type} }$', fontsize = 14)
ax1.tick_params(axis='both', which='major', labelsize=14)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

lines = lines_1 + lines_2
labels = labels_1 + labels_2

ax1.legend(lines, labels, loc=0)

#plt.grid(axis='y')
# ax1.legend()
# ax2.legend(loc=[0.85,0.5])

current_values = plt.gca().get_xticks()
# using format string '{:.0f}' here but you can choose others
plt.gca().set_xticklabels(['{:,.0%}'.format(x/10) for x in current_values])
#plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

plt.tight_layout()

#plt.grid(linestyle='dotted')
#plt.savefig(f'../../output/figures/fairness-factor-FEE*-{workload}.pdf',dpi=300)
plt.show()      
    
    
    
    