import uuid
import numpy as np
import pandas as pd
from umap import UMAP
from sklearn.cluster import KMeans
from ..base import TransformerMixin
from ._base_cluster import Cluster
from ._sampling import Sampler
from ..walmart_llm import BGEEmbedModel
from topicgpt.generation import TopicGenerator
# fill fileds: (id, parent_id, children_id, size, percentage)

class KmeansClustering(TransformerMixin):

    def __init__(self, n_neighbors, reduced_dim, n_clusters_list, sampler_mode,
                 model_name, temperature, batch_size, topk):
        self.n_neighbors = n_neighbors
        self.reduced_dim = reduced_dim
        self.n_clusters_list = n_clusters_list
        self.sampler = Sampler(mode=sampler_mode)
        self.embed_model = BGEEmbedModel(batch_size=500, device='mps')
        self.generator = TopicGenerator(model_name=model_name, temperature=temperature,
                                        batch_size=batch_size, topk=topk)
        self.cluster_dict = {}

    def transform(self, data_df):
        micro_clusters = self.do_micro_clustering(data_df, self.n_clusters_list[0])
        self.generator.transform(micro_clusters)

        micro_clusters_data = self.combine_data_and_embeddings(micro_clusters)
        sub_clusters = self.do_upper_clustering(micro_clusters_data, micro_clusters, self.n_clusters_list[1])
        self.generator.transform(sub_clusters)

        sub_clusters_data = self.combine_data_and_embeddings(sub_clusters)
        topic_clusters = self.do_upper_clustering(sub_clusters_data, sub_clusters, self.n_clusters_list[2])
        self.generator.transform(topic_clusters)

        root_clusters = [Cluster(id=str(uuid.uuid4()), data=data_df, size=len(data_df), percentage=1.0, ranked_idx=self.sampler.transform(data_df))]
        self.generator.transform(root_clusters)
        root_clusters[0].children_id = [cluster.id for cluster in topic_clusters]
        for cluster in topic_clusters:
            cluster.parent_id = root_clusters[0].id
            cluster.percentage = round(cluster.size/root_clusters[0].size, 3)

        return [root_clusters, topic_clusters, sub_clusters, micro_clusters]

    def do_micro_clustering(self, data_df, n_clusters):
        cluster_data_df = data_df.copy(deep=True)
        reducer = UMAP(n_neighbors=self.n_neighbors, n_components=self.reduced_dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(np.array(cluster_data_df['embeddings'].tolist(), dtype=np.float32))
        model = KMeans(n_clusters=min(n_clusters, len(cluster_data_df)), random_state=42, n_init="auto")
        model.fit(reduced_embeddings)
        cluster_data_df['cluster'] = model.labels_
        
        clusters = []
        for label in sorted(set(model.labels_)):
            tmp_data = cluster_data_df[cluster_data_df['cluster'] == label].reset_index(drop=True).drop(columns=['cluster'])
            tmp_cluster = Cluster(id=str(uuid.uuid4()), data=tmp_data, size=len(tmp_data), ranked_idx=self.sampler.transform(tmp_data))
            clusters.append(tmp_cluster)
        return clusters
    
    def combine_data_and_embeddings(self, clusters):
        texts, ids = [], []
        for cluster in clusters:
            texts.append(f"Topic: {cluster.topic}; Description: {cluster.description}; Summary: {cluster.summary}")
            ids.append(cluster.id)
        embeddings = self.embed_model.embed_documents(texts)
        return pd.DataFrame({'input': texts, 'embeddings': embeddings, 'id': ids})
    
    def do_upper_clustering(self, data_df, lower_clusters, n_clusters):
        cluster_data_df = data_df.copy(deep=True)
        reducer = UMAP(n_neighbors=self.n_neighbors, n_components=self.reduced_dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(np.array(cluster_data_df['embeddings'].tolist(), dtype=np.float32))
        model = KMeans(n_clusters=min(n_clusters, len(cluster_data_df)), random_state=42, n_init="auto")
        model.fit(reduced_embeddings)
        cluster_data_df['cluster'] = model.labels_

        clusters = []
        for label in sorted(set(model.labels_)):
            tmp_data = []
            for lower_cluster in lower_clusters:
                if lower_cluster.id in cluster_data_df[cluster_data_df['cluster'] == label]['id'].tolist():
                    tmp_data.append(lower_cluster.data)
            tmp_data = pd.concat(tmp_data, ignore_index=True)
            tmp_cluster = Cluster(id=str(uuid.uuid4()), data=tmp_data, size=len(tmp_data), ranked_idx=self.sampler.transform(tmp_data))
            tmp_cluster.children_id = cluster_data_df[cluster_data_df['cluster'] == label]['id'].tolist()
            for lower_cluster in lower_clusters:
                if lower_cluster.id in cluster_data_df[cluster_data_df['cluster'] == label]['id'].tolist():
                    lower_cluster.parent_id = tmp_cluster.id
                    lower_cluster.percentage = round(lower_cluster.size/tmp_cluster.size, 3)
            clusters.append(tmp_cluster)
        return clusters
    

class KmeansClustering_1(TransformerMixin):

    def __init__(self, n_neighbors, reduced_dim, n_clusters_list, sampler_mode,
                 model_name, temperature, batch_size, topk):
        self.n_neighbors = n_neighbors
        self.reduced_dim = reduced_dim
        self.n_clusters_list = n_clusters_list
        self.sampler = Sampler(mode=sampler_mode)
        self.embed_model = BGEEmbedModel(batch_size=500, device='mps')
        self.generator = TopicGenerator(model_name=model_name, temperature=temperature,
                                        batch_size=batch_size, topk=topk)
        self.cluster_dict = {}

    def transform(self, data_df):
        print("-micro-")
        micro_clusters = self.do_micro_clustering(data_df, self.n_clusters_list[0])
        self.generator.transform_from_dict(self.cluster_dict)
        print("-sub-")
        micro_clusters_data = self.combine_data_and_embeddings(micro_clusters)
        sub_clusters = self.do_upper_clustering(micro_clusters_data, micro_clusters, self.n_clusters_list[1])
        self.generator.transform_from_dict(self.cluster_dict)
        print("-topic-")
        sub_clusters_data = self.combine_data_and_embeddings(sub_clusters)
        topic_clusters = self.do_upper_clustering(sub_clusters_data, sub_clusters, self.n_clusters_list[2])
        self.generator.transform_from_dict(self.cluster_dict)
        print("-root-")
        root_clusters = [Cluster(id=str(uuid.uuid4()), data=data_df, size=len(data_df), percentage=1.0, ranked_idx=self.sampler.transform(data_df))]
        self.cluster_dict[root_clusters[0].id] = root_clusters[0]
        self.generator.transform_from_dict(self.cluster_dict)
        root_clusters[0].children_id = [cluster.id for cluster in topic_clusters]
        for cluster in topic_clusters:
            cluster.parent_id = root_clusters[0].id
            cluster.percentage = round(cluster.size/root_clusters[0].size, 3)

        return [root_clusters, topic_clusters, sub_clusters, micro_clusters]

    def do_micro_clustering(self, data_df, n_clusters):
        cluster_data_df = data_df.copy(deep=True)
        reducer = UMAP(n_neighbors=self.n_neighbors, n_components=self.reduced_dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(np.array(cluster_data_df['embeddings'].tolist(), dtype=np.float32))
        model = KMeans(n_clusters=min(n_clusters, len(cluster_data_df)), random_state=42, n_init="auto")
        model.fit(reduced_embeddings)
        cluster_data_df['cluster'] = model.labels_
        
        clusters = []
        for label in sorted(set(model.labels_)):
            tmp_data = cluster_data_df[cluster_data_df['cluster'] == label].reset_index(drop=True).drop(columns=['cluster'])
            tmp_cluster = Cluster(id=str(uuid.uuid4()), data=tmp_data, size=len(tmp_data), ranked_idx=self.sampler.transform(tmp_data))
            clusters.append(tmp_cluster)
            self.cluster_dict[tmp_cluster.id] = tmp_cluster
        return clusters
    
    def combine_data_and_embeddings(self, clusters):
        texts, ids = [], []
        for cluster in clusters:
            texts.append(f"Topic: {cluster.topic}; Description: {cluster.description}; Summary: {cluster.summary}")
            ids.append(cluster.id)
        embeddings = self.embed_model.embed_documents(texts)
        return pd.DataFrame({'input': texts, 'embeddings': embeddings, 'id': ids})
    
    def do_upper_clustering(self, data_df, lower_clusters, n_clusters):
        cluster_data_df = data_df.copy(deep=True)
        reducer = UMAP(n_neighbors=self.n_neighbors, n_components=self.reduced_dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(np.array(cluster_data_df['embeddings'].tolist(), dtype=np.float32))
        model = KMeans(n_clusters=min(n_clusters, len(cluster_data_df)), random_state=42, n_init="auto")
        model.fit(reduced_embeddings)
        cluster_data_df['cluster'] = model.labels_

        clusters = []
        for label in sorted(set(model.labels_)):
            tmp_data = []
            for lower_cluster in lower_clusters:
                if lower_cluster.id in cluster_data_df[cluster_data_df['cluster'] == label]['id'].tolist():
                    tmp_data.append(lower_cluster.data)
            tmp_data = pd.concat(tmp_data, ignore_index=True)
            tmp_cluster = Cluster(id=str(uuid.uuid4()), data=tmp_data, size=len(tmp_data), ranked_idx=self.sampler.transform(tmp_data))
            tmp_cluster.children_id = cluster_data_df[cluster_data_df['cluster'] == label]['id'].tolist()
            for lower_cluster in lower_clusters:
                if lower_cluster.id in cluster_data_df[cluster_data_df['cluster'] == label]['id'].tolist():
                    lower_cluster.parent_id = tmp_cluster.id
                    lower_cluster.percentage = round(lower_cluster.size/tmp_cluster.size, 3)
            clusters.append(tmp_cluster)
            self.cluster_dict[tmp_cluster.id] = tmp_cluster
        return clusters
                    