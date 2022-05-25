import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
from collections import Counter
from yellowbrick.cluster import KElbowVisualizer





def read_data(het_id):    
    path = f'../workload/execution_times/etc/etc-het-{het_id}.csv'
    df = pd.read_csv(path, index_col = ['Unnamed: 0'])
    S_T = df.max(axis=0) / df
    S_M = df.divide(df.max(axis=1), axis=0)
    S_M = 1 / S_M
    
    x1 = S_M.values.flatten()
    x2 = S_T.values.flatten()
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    
    return S_T, S_M , X

 

def clustering(X, n_clusters):    
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_
    return centroids, labels



def weighted_average(labels, centroids):
    total_size = len(labels)
    counts = Counter(labels)
    weighted_centroids = np.zeros(centroids.shape)
    weights = np.zeros(centroids.shape[0])
    for i in range(centroids.shape[0]):
        weights[i] = counts[i] / total_size
        weighted_centroids[i] = weights[i]* centroids[i]
    weighted_avg = weighted_centroids.sum(axis=0)
    
    return weighted_avg, weights


def resultant(X):
    R = X.mean(axis=0)
    


def optimal_clusters(X, max_clusters):  
    # s_scores = []
    # #d_scores = []
    # for k in range(2,10):
    #     kmeans = KMeans(n_clusters=k).fit(X)        
    #     s_score = metrics.silhouette_score(X, kmeans.labels_) 
    #     #d_score = metrics.davies_bouldin_score (X, kmeans.labels_)
    #     s_scores.append(s_score)
    #     #d_scores.append(d_score)
    
    
    # optimal_s = np.argmax(s_scores) + 2
    # #optimal_d = np.argmin(d_scores) + 2
    # optimal_d = 0
    
    # optimal_n_clusters = max (optimal_s, optimal_d)
    
    
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,10))
    
    visualizer.fit(X)        # Fit the data to the visualizer
    visualizer.show()


    optimal_n_clusters = visualizer.elbow_value_
    
    
    return optimal_n_clusters
        
    
#def plot_results(het_id, X, labels, centroids, weighted_avg, saved=False):         
def plot_results(het_id, X, avg, saved=False):         
    plt.figure()
    # cmap = get_cmap('brg')    
    # norm = Normalize(vmin=0.0, vmax=len(np.unique(labels))-1) 
    # for g in np.unique(labels):
    #     ix = np.where(labels == g)               
    #     rgba = cmap(norm(g)) 
    #     plt.scatter(X[ix,0], X[ix,1], color= rgba, label= f'C{g}')           
    #     plt.scatter(centroids[g, 0],centroids[g, 1],marker='+',color ='k', s=400)        
    plt.scatter(X[:,0], X[:,1])           
    plt.scatter(avg[0],avg[1],marker='*',color ='r', s=500)
   
    #plt.legend(markerscale = 2, prop={'size': 18})
    
    
    plt.xlabel(f'machine affinity, '+ r'$H^M$', fontsize=14)
    plt.ylabel(f'task affinity, '+ r'$H^T$', fontsize=14)
    plt.grid(which='major', axis='both', linestyle=':')
    #plt.ylim(0,10)
    plt.tight_layout()
    
    if saved :
        plt.savefig(f'../workload/heterogeneous/etc_{het_id}.pdf', dpi=300)
        plt.savefig(f'../workload/heterogeneous/etc_{het_id}.jpg', dpi=300)

def heterogeneity_level(het_id, saved=False):    
    s_t, s_m,  X = read_data(het_id)
    #max_clusters = s_t.shape[0] * s_t.shape[1]
    #optimal_n_clusters = optimal_clusters(X, max_clusters)
    #centroids, labels = clustering(X, optimal_n_clusters)
    #weighted_avg, weights = weighted_average(labels, centroids)
    avg = X.mean(axis = 0)
    # H_index = np.linalg.norm(weighted_avg) / np.sqrt(2.0)    
    H_index = np.linalg.norm(avg) / np.sqrt(2.0)    
    # plot_results(het_id, X, labels, centroids, weighted_avg, saved)    
    plot_results(het_id, X, avg, saved)    
    
    #return H_index, optimal_n_clusters, X, centroids, labels
    return H_index, X
    
    

# H_index,  X = heterogeneity_level(5)






