import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np
import seaborn as sns


SEPs = ['1_75']
etcs = list(range(30))
scheduler = 'MM'
scenario = 'sc-4'


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h



base_path = f'../output/data/{scenario}/heterogeneous'
df_summary = pd.DataFrame(columns=['SEP','etc_id','completion%'])

for SEP in SEPs:
    path_to_SEP = f'{base_path}/{SEP}'
    hindices = pd.read_csv(f'../task_machine_performance/heterogeneous/{SEP}/hindices.csv')
    

    for etc_id in etcs:
        sep = hindices[hindices['etc_id']==f'etc-{etc_id}']['SEP'].values[0]
        path = f'{path_to_SEP}/etc_{etc_id}/{scheduler}/results-summary.csv'
        df = pd.read_csv(path, usecols=['totalCompletion%'])
        avg_completion = df.mean().loc['totalCompletion%']
        d = {'SEP':sep,
             'etc_id':etc_id,
             'completion%':avg_completion}
        df_summary = df_summary.append(d, ignore_index = True)

C = df_summary['completion%'].values

h = mean_confidence_interval(C)

#plt.boxplot(C)

# Cut the window in 2 parts
f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
# Add a graph in each part
sns.boxplot(C, ax=ax_box)
sns.displot(C, ax=ax_hist, kind='ecdf')
 
# Remove x axis name for the boxplot
ax_box.set(xlabel='')
plt.figure()
plt.scatter(df_summary['SEP'].values, df_summary['completion%'].values)
plt.xlabel('SEP')
plt.ylabel('Completion(%)')