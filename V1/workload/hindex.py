from matplotlib.cbook import flatten
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from collections import Counter
from yellowbrick.cluster import KElbowVisualizer


class HINDEX:


    def __init__(self, name):
        self.name = name

    def read_data(self, etc_id):    
        path_to_etc = f'./workload/etcs/{self.name}/{etc_id}.csv'
        df = pd.read_csv(path_to_etc, index_col = ['Unnamed: 0'])
        #mu = df.mean().mean()
        S_T = df.max(axis=0) / df
        S_M = df.divide(df.max(axis=1), axis=0)
        S_M = 1 / S_M

        mean_s_m = df.max(axis=1).mean()
        mean_s_t = df.max(axis=0).mean()

        
        
        sm_flatten = S_M.values.flatten()
        st_flatten = S_T.values.flatten()
        flattened = np.array(list(zip(sm_flatten, st_flatten))).reshape(len(sm_flatten), 2)
        
        return S_T, S_M , flattened, mean_s_m, mean_s_t

    

    def clustering(self, flattened, n_clusters):    
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(flattened)
        labels = kmeans.predict(flattened)
        centroids = kmeans.cluster_centers_
        return centroids, labels


    def weighted_average(self, labels, centroids):
        total_size = len(labels)
        counts = Counter(labels)
        weighted_centroids = np.zeros(centroids.shape)
        weights = np.zeros(centroids.shape[0])
        for i in range(centroids.shape[0]):
            weights[i] = counts[i] / total_size
            weighted_centroids[i] = weights[i]* centroids[i]
        weighted_avg = weighted_centroids.sum(axis=0)
        
        return weighted_avg, weights

    def optimal_clusters(self, flattened, max_clusters):  
        model = KMeans()
        visualizer = KElbowVisualizer(model, k=(2,max_clusters))        
        visualizer.fit(flattened)        
        visualizer.show()
        optimal_n_clusters = visualizer.elbow_value_
        return optimal_n_clusters
            
     
             
    def plot(self, etc_id, flattened, avg, saved=False):         
        plt.figure()
        # cmap = get_cmap('brg')    
        # norm = Normalize(vmin=0.0, vmax=len(np.unique(labels))-1) 
        # for g in np.unique(labels):
        #     ix = np.where(labels == g)               
        #     rgba = cmap(norm(g)) 
        #     plt.scatter(X[ix,0], X[ix,1], color= rgba, label= f'C{g}')           
        #     plt.scatter(centroids[g, 0],centroids[g, 1],marker='+',color ='k', s=400)        
        plt.scatter(flattened[:,0], flattened[:,1])           
        plt.scatter(avg[0],avg[1],marker='*',color ='r', s=500)    
        #plt.legend(markerscale = 2, prop={'size': 18})        
        plt.xlabel(f'machine affinity, '+ r'$H^M$', fontsize=14)
        plt.ylabel(f'task affinity, '+ r'$H^T$', fontsize=14)
        plt.grid(which='major', axis='both', linestyle=':')
        #plt.ylim(0,10)
        plt.tight_layout()
        
        if saved :
            plt.savefig(f'./output/figures/{self.name}-etcs/{etc_id}.pdf', dpi=300)
            plt.savefig(f'./output/figures/{self.name}-etcs/{etc_id}.jpg', dpi=300)

    def hindex(self, etc_id, saved=False):    
        _, _,  flattened, mean_s_m, mean_s_t = self.read_data(etc_id)        
        speedup = flattened.mean(axis = 0)
        # h = np.zeros(avg.shape)
        # h[0] = mean_s_m / avg[0]
        # h[1] = mean_s_t / avg[1] 
        h_index = np.linalg.norm([mean_s_m, mean_s_t]) / np.linalg.norm(speedup)
        #h_index = np.linalg.norm([mean_s_m/speedup[0], mean_s_t/speedup[1]]) 
        #self.plot(etc_id, flattened, avg, saved)
        

        return  h_index , np.linalg.norm(speedup)





