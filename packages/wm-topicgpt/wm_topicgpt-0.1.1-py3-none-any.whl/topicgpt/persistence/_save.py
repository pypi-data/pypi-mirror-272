import json
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from google.oauth2.service_account import Credentials


select_cols = ['topic', 'topic_desc', 'topic_summary', 'topic_keywords', 
               'subtopic', 'subtopic_desc', 'subtopic_summary', 'subtopic_keywords',
               'microtopic', 'microtopic_desc', 'microtopic_summary', 'microtopic_keywords']


def transform_data_format(clusters_list, dataset_name):
    saved_data = clusters_list[0][0].data.copy(deep=True)
    saved_data['dataset_name'] = dataset_name
    saved_data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for col in select_cols:
        saved_data[col] = ""

    for level, clusters in enumerate(clusters_list[1:], 1):
        if level == 1:
            topic, desc, summary, keywords = select_cols[:4]
        elif level == 2:
            topic, desc, summary, keywords = select_cols[4:8]
        elif level == 3:
            topic, desc, summary, keywords = select_cols[8:12]
        
        for cluster in clusters:
            for row in cluster.data.iterrows():
                cond = saved_data['uuid'] == row[1]['uuid']
                saved_data.loc[cond, topic] = cluster.topic
                saved_data.loc[cond, desc] = cluster.description
                saved_data.loc[cond, summary] = cluster.summary
                saved_data.loc[cond, keywords] = str(cluster.keywords)
    
    return saved_data


def transform_topic_format(clusters_list, dataset_name):
    topics = []
    for idx, clusters in enumerate(clusters_list):
        for cluster in clusters:
            topics.append(
                {'id': cluster.id, 'topic': cluster.topic, 'description': cluster.description, 'summary': cluster.summary,
                 'keywords': cluster.keywords, 'parent_id': cluster.parent_id, 'children_id': cluster.children_id,
                 'level': idx, 'size': cluster.size, 'percentage': cluster.percentage, 'dataset_name': dataset_name
                }
            )
    topic_df = pd.DataFrame(topics)
    topic_df['dataset_name'] = dataset_name
    topic_df['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return topic_df


def save_data_to_bq(data_df, credential_path, params):
    # transform dataframe
    new_select_cols = ['input'] + select_cols
    metadata_cols = [col for col in data_df.columns if col not in new_select_cols]
    data_df['metadata'] = str(data_df[metadata_cols].apply(lambda x: x.to_dict(), axis=1))
    keep_data_df = data_df[new_select_cols+['metadata']]

    # Load credential
    with open(credential_path, "r") as f:
        credential_info = json.loads(f.read())

    # Create client
    credentials = Credentials.from_service_account_info(credential_info)
    client = bigquery.Client(credentials=credentials)

    # create a table
    schema = [
        bigquery.SchemaField(field_name, 'STRING') for field_name in keep_data_df.columns
    ]
    table_ref = client.dataset(params['dataset_id']).table(params['table_id'])
    try:
        table = client.get_table(table_ref)
    except Exception as e:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Table created! ")
    
    # save to bq
    job = client.load_table_from_dataframe(keep_data_df, table)
    job.result()
    assert job.state == "DONE"


def save_time_to_bq(time_dict, credential_path, params):
    keep_data_df = pd.DataFrame([time_dict])
    
    # Load credential
    with open(credential_path, "r") as f:
        credential_info = json.loads(f.read())

    # Create client
    credentials = Credentials.from_service_account_info(credential_info)
    client = bigquery.Client(credentials=credentials)

    # create a table
    schema = [
        bigquery.SchemaField(field_name, 'STRING') for field_name in keep_data_df.columns
    ]
    table_ref = client.dataset(params['dataset_id']).table(params['time_id'])
    try:
        table = client.get_table(table_ref)
    except Exception as e:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Table created! ")
    
    # save to bq
    job = client.load_table_from_dataframe(keep_data_df, table)
    job.result()
    assert job.state == "DONE"
