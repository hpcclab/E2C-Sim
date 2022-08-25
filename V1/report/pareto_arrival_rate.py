import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np



def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h
    


schedulers = ['FEE','EE','MM','MMU','MSD']

task_hete = 0

df_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'totalCompletion%', 'consumed_energy%'])

yerr_summary = pd.DataFrame(data=None, columns = ['rate-id','scheduler' ,'totalCompletion%','consumed_energy%'])

hatch = [['++','\\\\\\'],['///', 'xxx']]
#colors = [['seagreen','darkorange'],['salmon','darkcyan']]
#colors = [['seagreen','darkslateblue'],['salmon','darkcyan']]

colors = ['navy','darkred','orange', 'purple','darkgreen']
markers = ['o','x','<','+','s']

objective = ['total_completion']

for scheduler in schedulers:
        
    for rate in [0,1,2,3,4,5,6,7,8,9]:
    
        workload = f'{rate}-{task_hete}'
        path = f'../../output/data/{workload}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path, usecols=['totalCompletion%', 'consumed_energy%'])        
        
        
        d = df.mean().loc[['totalCompletion%', 'consumed_energy%']]        
        d['rate-id'] = int(rate)        
        d['scheduler'] = scheduler
        
        #yerr_compl = mean_confidence_interval(df['totalCompletion%'].values)
        #yerr_energy = mean_confidence_interval(df['consumed_energy%'].values)
        
        # d_err = {'totalCompletion%':yerr_compl,
        #          'consumed_energy%':yerr_energy,
        #         'rate-id':rate,
        #         'scheduler':scheduler
        #                 }
        # yerr_summary = yerr_summary.append(d_err, ignore_index=True)
        df_summary = df_summary.append(d, ignore_index=True)
        df_summary['rate-id'] = df_summary['rate-id'].astype('int')
    

rate_label = [round(2000/x,1) for x in [1000, 800, 667, 500, 400, 333, 250, 200, 100,20]]

rate_label.sort()

plt.figure()
i=0

for scheduler in schedulers:
    
    results = df_summary[df_summary['scheduler']==scheduler]
    
    if scheduler == 'EE':
        label = 'ELARE'
    elif scheduler == 'FEE':
        label = 'FELARE'
    else:
        label = scheduler
    
    consumed_energy = results['consumed_energy%'].values
    total_completion = results['totalCompletion%'].values
    plt.plot(consumed_energy, 100-total_completion, 
             marker = markers[i],
             color= colors[i],
             linestyle='-',
            label = label)
    
    if scheduler == 'EE':
        plt.fill_betweenx(100-total_completion,consumed_energy, x2=100,color= 'lightgrey',
                          alpha=0.5, interpolate=True)
        bbox = dict(boxstyle ="round", fc ="white", color = 'k',pad=0.5)
        plt.annotate('dominated solutions',
                        xy = (80,60), xytext =(70,80),color='k',
                        #textcoords ='offset points',
                        bbox = bbox,horizontalalignment='center',fontsize=12) 
        
        bbox = dict(boxstyle ="round", fc ="none", color='k')
        arrowprops = dict(
            arrowstyle = "->", lw = 1.3,
            connectionstyle = "angle, angleA = 0, angleB = 90,\
            rad = 10",
            )
        
            
        
        for _, row in results.iterrows():
            rate = row['rate-id']
            loc = row[['consumed_energy%','totalCompletion%']].values
            loc[1] = 100 - loc[1]
            
            
            print(i, rate)
            
            if i==1 and rate == 3:
                
                xdata, ydata = loc[0], loc[1]
                #xdisplay, ydisplay = plt.transData.transform((xdata, ydata))
                  
                bbox = dict(boxstyle ="round", fc ="none", color='k', pad=0.6)
                arrowprops = dict(
                    arrowstyle = "->", lw = 1.3,color='k',
                    connectionstyle = "angle, angleA = 0, angleB = 90,\
                    rad = 10",
                    )
                  
                offset = -20
                
                # Annotation
                plt.annotate('Pareto front',
                            xy = (xdata-2, ydata+2), xytext =(20,20),color='k',
                            #textcoords ='offset points',
                            bbox = bbox, arrowprops = arrowprops, rotation = 0,
                            horizontalalignment='center',fontsize=12) 
            
            # plt.annotate('%1.0f'%(rate_label[rate]),
            #             xy = (loc[0]+1,loc[1]-10), #xytext =(35,30),
            #             #textcoords ='offset points',
            #            ) 
            
            # plt.annotate('arrival rate > %.1f'%(rate_label[rate]),
            #             xy = (30,30), xytext =(5,65),
            #             #textcoords ='offset points',
            #             bbox = bbox, rotation = -25) 
            
            #plt.annotate(str(rate_label[rate]), loc)
        #plt.annotate('arrival rates',[30,30])
    i+=1


plt.xlabel('%energy consumption', fontsize= 14)
plt.ylabel('%unsuccessful tasks', fontsize= 14)
plt.xlim(0,100)
plt.ylim(0,100)
plt.legend(loc=(0.78,0.1))
plt.tight_layout()
#plt.savefig(f'../../output/figures/revised_with_more_arrivals/pareto_arrivalrates_more_heuristics.pdf',dpi=300)
   


