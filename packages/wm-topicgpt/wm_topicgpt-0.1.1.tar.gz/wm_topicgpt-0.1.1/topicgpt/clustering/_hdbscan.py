import uuid
import numpy as np
from umap import UMAP
from sklearn.cluster import HDBSCAN
from ..base import TransformerMixin
from ._base_cluster import Cluster
from ._sampling import Sampler

# fill fileds: (id, parent_id, children_id, size, percentage, ranked_idx)

class HDBSCANClustering(TransformerMixin):

    def __init__(self, reduced_dim, n_neighbors, min_cluster_percent, sampler_mode):
        self.reduced_dim = reduced_dim
        self.n_neighbors = n_neighbors
        if n_neighbors < 10:
            raise ValueError("`n_neighbors` should be larger than 10!")
        self.min_cluster_percent = min_cluster_percent
        self.sampler = Sampler(mode=sampler_mode)

    def transform(self, data_df):
        self.min_cluster_size = int(self.min_cluster_percent * len(data_df))

        root = Cluster(id=str(uuid.uuid4()), data=data_df, size=len(data_df), percentage=1.0, ranked_idx=self.sampler.transform(data_df))
        topic_clusters = self.do_clustering(root, self.n_neighbors)
        root.children_id = [tmp_cluster.id for tmp_cluster in topic_clusters]

        sub_clusters = []
        self.n_neighbors = int(self.n_neighbors / 2)
        for cluster in topic_clusters:
            if cluster.size >= self.min_cluster_size:
                tmp_clusters = self.do_clustering(cluster, self.n_neighbors)
                cluster.children_id = [tmp_cluster.id for tmp_cluster in tmp_clusters]
                sub_clusters.extend(tmp_clusters)

        micro_clusters = []
        self.n_neighbors = int(self.n_neighbors / 2)
        for cluster in sub_clusters:
            if cluster.size >= self.min_cluster_size:
                tmp_clusters = self.do_clustering(cluster, self.n_neighbors)
                cluster.children_id = [tmp_cluster.id for tmp_cluster in tmp_clusters]
                micro_clusters.extend(tmp_clusters)

        return [[root], topic_clusters, sub_clusters, micro_clusters]

    def do_clustering(self, cluster, n_neighbors):
        cluster_data_df = cluster.data.copy()
        reducer = UMAP(n_neighbors=n_neighbors, n_components=self.reduced_dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(np.array(cluster_data_df['embeddings'].tolist(), dtype=np.float32))
        model = HDBSCAN(min_cluster_size=self.min_cluster_size, min_samples=min(self.n_neighbors, len(cluster_data_df)), n_jobs=-1)
        model.fit(reduced_embeddings)
        cluster_data_df['cluster'] = model.labels_
        
        sub_clusters = []
        if len(set(model.labels_)) > 1:
            for label in sorted(set(model.labels_)):
                tmp_data = cluster_data_df[cluster_data_df['cluster'] == label].reset_index(drop=True).drop(columns=['cluster'])
                sub_clusters.append(
                    Cluster(id=str(uuid.uuid4()), data=tmp_data, parent_id=cluster.id, size=len(tmp_data), 
                            percentage=round(len(tmp_data)/len(cluster_data_df), 3), ranked_idx=self.sampler.transform(tmp_data))
                )
        return sub_clusters