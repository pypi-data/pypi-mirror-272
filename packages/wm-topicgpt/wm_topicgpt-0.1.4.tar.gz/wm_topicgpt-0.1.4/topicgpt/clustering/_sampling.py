import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
from ..base import TransformerMixin


class Sampler(TransformerMixin):

    def __init__(self, mode="mmr", diversity=0.7):
        self.mode = mode
        self.diversity = diversity

    def transform(self, data_df):
        if self.mode == 'centroid':
            return self.sampling_centroids(data_df)
        elif self.mode == 'similarity':
            return self.sampling_maximum_similarity(data_df)
        elif self.mode == 'mmr':
            return self.sampling_maximum_marginal_relevance(data_df, self.diversity)
        else:
            raise ValueError(f"Don't support `{self.mode}` mode")
        
    def sampling_centroids(self, data_df):
        centroid = np.mean(np.array(data_df['embeddings'].tolist(), dtype=np.float32), axis=0)
        dists = pairwise_distances(np.array([centroid], dtype=np.float32), np.array(data_df['embeddings'].tolist(), dtype=np.float32))[0]
        ranked_idx = np.argsort(dists)
        return ranked_idx
    
    def sampling_maximum_similarity(self, data_df):
        candidate_d = cosine_similarity(data_df['embeddings'].tolist(), data_df['embeddings'].tolist())
        ranked_idx = np.argsort(candidate_d.sum(axis=1))
        return ranked_idx
    
    def sampling_maximum_marginal_relevance(self, data_df, diversity):
        # find the most representative documents
        candidate_d = cosine_similarity(data_df['embeddings'].tolist(), data_df['embeddings'].tolist())
        ranked_idx = [np.argmax(candidate_d.sum(axis=1))]
        candidates_idx = [i for i in range(len(data_df)) if i != ranked_idx[0]]

        # filter based on maximal marginal relevance
        for _ in range(len(data_df)-1):
            candidate_similarities = candidate_d.sum(axis=1)[candidates_idx]
            target_similarities = np.max(candidate_d[candidates_idx][:, ranked_idx], axis=1)

            # calculate MMR
            mmr = (1 - diversity) * candidate_similarities - diversity * target_similarities
            # update keywords & candidates
            mmr_idx = candidates_idx[np.argmax(mmr)]
            ranked_idx.append(mmr_idx)
            candidates_idx.remove(mmr_idx)
        return ranked_idx