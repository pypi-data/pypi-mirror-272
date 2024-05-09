import os
import uuid
import pandas as pd

params = {
    'preprocessing': {'words_range': (2, 500)},
    'name_filter': {},
    'embedding': {'model': 'bge', 'batch_size': 500, 'device': 'mps'},
    'clustering':{
        'model': 'hdbscan',
        'hdbscan': {'reduced_dim': 5, 'n_neighbors': 10, 'min_cluster_percent': 0.01, 'sampler': 'similarity'},
        'kmeans': {'reduced_dim': 5, 'n_neighbors': 10, 'n_clusters_list': [50, 15, 5], 'sampler': 'similarity'},
        'topic': {'model_name': "gpt-35-turbo-16k", 'temperature': 0.5, 'batch_size': 5, 'topk': 10},
    },
    'keywords': {'ngram_range': (1, 2), 'topk': 10},
    'save_file': {'data_file': '../save/data.csv', 'topic_file': '../save/topic.csv', 'plot_file': '../save/tree.txt'},
    'bigquery': {'dataset_id': 'analytics', 'table_id': 'topic_modeling_data', 'time_id': 'topic_modeling_time'},
}


def topic_modeling(data_file, col_name, params=params):
    # load data
    dataset_name = os.path.basename(data_file).split(".")[0]
    file_extension = os.path.splitext(data_file)[1].lower()
    if file_extension == '.csv':
        data_df = pd.read_csv(data_file)
    elif file_extension == '.xlsx' or file_extension == '.xls':
        data_df = pd.read_excel(data_file)

    # data transform 
    data_df = data_df.rename(columns={col_name: 'input'})
    data_df = data_df.dropna(subset=["input"])
    data_df['input'] = data_df['input'].astype(str)
    data_df['uuid'] = [str(uuid.uuid4()) for _ in range(len(data_df))]

    # preprocessing and pii_filter
    print("Step 1: Preprocessing")
    from topicgpt.preprocessing import MinMaxLengthFilter, NameFilter
    filter = MinMaxLengthFilter(words_range=params['preprocessing']['words_range'])
    data_df = filter.transform(data_df)
    filter = NameFilter()
    data_df = filter.transform(data_df)

    # embedding
    print("Step 2: Embedding")
    from topicgpt.walmart_llm import AdaEmbedModel, BGEEmbedModel
    if params['embedding']['model'] == 'ada':
        llm = AdaEmbedModel(batch_size=params['embedding']['batch_size'])
    elif params['embedding']['model'] == 'bge':
        llm = BGEEmbedModel(batch_size=params['embedding']['batch_size'], device=params['embedding']['device'])
    else:
        raise ValueError(f"Don't support {params['embedding']} model")
    embeddings = llm.embed_documents(data_df['input'].tolist())
    data_df['embeddings'] = embeddings
    data_df = data_df.dropna(subset=["embeddings"])

    # clustering
    from topicgpt.clustering import HDBSCANClustering
    if params['clustering']['model'] == 'hdbscan':
        print("Step 3: Clustering")
        model = HDBSCANClustering(reduced_dim=params['clustering']['hdbscan']['reduced_dim'], 
                                  n_neighbors=params['clustering']['hdbscan']['n_neighbors'], 
                                  min_cluster_percent=params['clustering']['hdbscan']['min_cluster_percent'],
                                  sampler_mode=params['clustering']['hdbscan']['sampler'])
        clusters_list = model.transform(data_df)
        
        # generate topic and description
        print("Step 4: Topic & Description & Summarization")
        from topicgpt.generation import TopicGenerator
        generator = TopicGenerator(model_name=params['clustering']['topic']['model_name'], 
                                   temperature=params['clustering']['topic']['temperature'],
                                   batch_size=params['clustering']['topic']['batch_size'], 
                                   topk=params['clustering']['topic']['topk'])
        generator.transform(clusters_list)
        
    elif params['clustering']['model'] == 'kmeans':
        print('Step 3 & 4: Clustering & Topic & Description & Summarization')
        from topicgpt.clustering import KmeansClustering
        model = KmeansClustering(n_neighbors=params['clustering']['kmeans']['n_neighbors'],
                                 reduced_dim=params['clustering']['kmeans']['reduced_dim'],
                                 n_clusters_list=params['clustering']['kmeans']['n_clusters_list'],
                                 sampler_mode=params['clustering']['kmeans']['sampler'],
                                 model_name=params['clustering']['topic']['model_name'], 
                                 temperature=params['clustering']['topic']['temperature'],
                                 batch_size=params['clustering']['topic']['batch_size'], 
                                 topk=params['clustering']['topic']['topk'])
        clusters_list = model.transform(data_df)

    # keywords for clusters
    print("Step 5: Keywords")
    from topicgpt.generation import KeywordsExtractor
    extractor = KeywordsExtractor(ngram_range=params['keywords']['ngram_range'], topk=params['keywords']['topk'])
    extractor.transform(clusters_list)

    # save the data
    print("Step 6: Save data to files")
    from topicgpt.persistence import transform_data_format, transform_topic_format, plot_topic_taxonomy_tree
    saved_data = transform_data_format(clusters_list, dataset_name)
    saved_data.to_csv(params['save_file']['data_file'], index=False)
    topic_data = transform_topic_format(clusters_list, dataset_name)
    topic_data.to_csv(params['save_file']['topic_file'], index=False)
    plot_topic_taxonomy_tree(clusters_list, params['save_file']['plot_file'])
