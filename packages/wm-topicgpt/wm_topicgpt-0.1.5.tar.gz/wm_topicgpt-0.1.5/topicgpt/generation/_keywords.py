from tqdm import tqdm
from keybert import KeyBERT
from ..base import TransformerMixin


class KeywordsExtractor(TransformerMixin):

    def __init__(self, ngram_range=(1, 2), topk=15):
        self.ngram_range = ngram_range
        self.topk = topk
        self.model = KeyBERT(model='all-MiniLM-L6-v2')
    
    # def transform(self, cluster_list):
    #     clusters = []
    #     for cluster in cluster_list:
    #         clusters.extend(cluster)
    #     # build document
    #     for cluster in tqdm(clusters, total=len(clusters)):
    #         doc = ". ".join(cluster.data['input'].tolist())
    #         print("--start", len(doc.split()))
    #         row_keywords = self.model.extract_keywords(
    #             doc, 
    #             keyphrase_ngram_range=self.ngram_range, 
    #             stop_words='english',
    #             use_mmr=True,
    #             diversity=0.8,
    #             top_n=self.topk
    #         )
    #         print("--end")
    #         cluster.keywords = [key[0] for key in row_keywords]

    def transform_row(self, data_df):
        keywords = []
        for content in tqdm(data_df['input'].tolist()):
            row_keywords = self.model.extract_keywords(
                str(content), 
                keyphrase_ngram_range=self.ngram_range, 
                stop_words=None,
                use_mmr=True,
                diversity=0.8,
                top_n=self.topk
            )
            keywords.append(str([key[0] for key in row_keywords]))
        data_df['keywords'] = keywords
            

    def transform(self, clusters_list):
        # leaves clusters
        leaves_cluster = []
        for clusters in clusters_list:
            for cluster in clusters:
                if len(cluster.children_id) == 0:
                    leaves_cluster.append(cluster)
        for cluster in tqdm(leaves_cluster, total=len(leaves_cluster)):
            doc = ". ".join(cluster.data['input'].tolist())
            doc = doc[:50000]
            row_keywords = self.model.extract_keywords(
                doc, 
                keyphrase_ngram_range=self.ngram_range, 
                # stop_words='english',
                stop_words=None,
                use_mmr=True,
                diversity=0.8,
                top_n=self.topk
            )
            cluster.keywords = [key[0] for key in row_keywords]

        # non leaves clusters
        sz = len(clusters_list)
        for idx in range(sz-1, -1, -1):
            for cluster in clusters_list[idx]:
                if cluster.keywords is None:
                    keywords = []
                    if len(cluster.children_id) > 0:
                        for sub_cluster in clusters_list[idx+1]:
                            if sub_cluster.id in cluster.children_id:
                                keywords.extend(sub_cluster.keywords)
                    cluster.keywords = keywords