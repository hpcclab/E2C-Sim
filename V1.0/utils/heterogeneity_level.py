from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


hete_level = 3
consistency_degree = 30

def read_data(hete_level, consistency_degree):
    path = f'../workload/heterogeneous/H_{hete_level}_a_{consistency_degree}.csv'
    
    df = pd.read_csv(path, index_col = ['task_types'])
    S_T = df.max(axis=0) / df
    S_M = df.divide(df.max(axis=1), axis=0)
    S_M = 1 / S_M
    
    

    return df,S_T, S_M
df, s_t, s_m = read_data(hete_level, consistency_degree)    

s_t
# Creating the data
# x1 = np.array([1.25,1,9.1,8.3,1,1,7.5,6.9,1.1,1,10,9.2,1.1,1,7.7,7.7])
# x2 = np.array([1.25,1.1,1.2,1.08,1.1,1.2,1.08,1.,1,1,1.2,1.08,1.1,1.1,1,1])
x1 = s_m.values.flatten()
x2 = s_t.values.flatten()
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)

#X = x2.reshape(-1,1)
 
# Visualizing the data
plt.plot()

plt.title('Dataset')
plt.scatter(x1, x2)
plt.xlabel(r'$S^M$'+f'\n speed-up due to M.T Hete.', fontsize=14)
plt.ylabel(r'$S^T$'+f'\n speed-up due to T.T Hete.', fontsize=14)
plt.axis('equal')
plt.show()


distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 10)
 
for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
 
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X.shape[0])
    inertias.append(kmeanModel.inertia_)
 
    mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                   'euclidean'), axis=1)) / X.shape[0]
    mapping2[k] = kmeanModel.inertia_
    
for key, val in mapping1.items():
    print(f'{key} : {val}')
    
plt.plot(K, distortions, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.show()

plt.plot(K, inertias, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Inertia')
plt.title('The Elbow Method using Inertia')
plt.show()

y_pred = KMeans(n_clusters=3, random_state=0).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred, alpha=0.7, s= 100, cmap='brg')
#plt.scatter([i for i in range(len(X))], X[:,0], c=y_pred, alpha=0.5, s= 100, cmap='brg')
#plt.axis('equal')
# x = []
m, b = np.polyfit(X[:, 0], X[:, 1], 1)
# x.append(np.min(x1))
# x.append(np.max(x1))
# x = np.array(x)
# plt.plot(x, m*x + b, 'r--', linewidth=2)
legend_properties = {'weight':'bold'}

sns.regplot(X[:, 0], X[:, 1], color = 'navy', marker='',label=f'Regression Line: {m:.2f}'+r' $S^T$'+f'+{b:.2f}')


#sns.jointplot(x=X[:, 0], y=X[:, 1],  kind="reg")
mx = max(max(x1),max(x2))
plt.xlim(0.8, 7)
plt.ylim(0.9, 5)
plt.legend(prop=legend_properties)

plt.xlabel(r'$S^M$'+f'\n speed-up due to M.T Hete.', fontsize=14)
plt.ylabel(r'$S^T$'+f'\n speed-up due to T.T Hete.', fontsize=14)
plt.grid(which='major', axis='both', linestyle=':')
plt.tight_layout()
plt.savefig(f'../workload/heterogeneous/H_{hete_level}_a_{consistency_degree}.pdf', dpi=300)
