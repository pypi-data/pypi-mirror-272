import tiktoken
import numpy as np
from ..base import TransformerMixin
from ..walmart_llm import ChatModel
from ..clustering import Cluster


topic_template = """Given one text delimited by triplet backquotes, your task is to generate a main topic of this text, a simple description of this topic, and a detailed summary of this text according to following requirements:

<Requirements>
1. The topic should be less than 10 words but detiled.
2. The description should be less than 30 words.
3. The summary should be in about 100 - 150 words.
</Requirements>

```{{text}}```

Output topic and description in JSON format as follows:
{"topic": <put the topic here>, "description": <put the description here>, "summary": <put the summary here>}"""

# summary_template = """Given one text delimited by triplet backquotes, your task is to generate a detailed summary for this text in 200 words.

# ```{{text}}```

# Output topic and description in JSON format as follows:
# {"summary": <put the summary here>}"""


class TopicGenerator(TransformerMixin):

    def __init__(self, model_name="gpt-35-turbo", temperature=0.5, batch_size=100, topk=20):
        self.topk = topk
        self.model = ChatModel(model_name=model_name, temperature=temperature, batch_size=batch_size)
        self.encoding = tiktoken.encoding_for_model(model_name=model_name)
        if model_name == 'gpt-35-turbo':
            self.max_token = 3000
        elif model_name == 'gpt-35-turbo-16k':
            self.max_token = 15000
        elif model_name == 'gpt-4':
            self.max_token = 7000
        else:
            raise ValueError(f"Don't support `{model_name}` model")
        
    def transform(self, clusters_list):
        clusters = []
        for cluster in clusters_list:
            if isinstance(cluster, list):
                clusters.extend(cluster)
            elif isinstance(cluster, Cluster):
                clusters.append(cluster)
            else:
                raise ValueError("Don't support this type!")
        
        # topic & description & summarization
        topic_prompts, summary_prompts = [], []
        for cluster in clusters:
            text = ""
            for idx in cluster.ranked_idx[:self.topk]:
                tmp_text = cluster.data.iloc[idx]['input']
                if len(self.encoding.encode(text+tmp_text)) > self.max_token:
                    break
                text += (tmp_text.strip() + "\n")
            topic_prompts.append(topic_template.replace("{{text}}", text))
            # summary_prompts.append(summary_template.replace("{{text}}", text))

        topic_responses = self.model.batch_completion(topic_prompts)
        # summary_responses = self.model.batch_completion(summary_prompts)
        for cluster, topic_response in zip(clusters, topic_responses):
            try:
                cluster.topic = eval(topic_response)['topic']
                cluster.description = eval(topic_response)['description']
                cluster.summary = eval(topic_response)['summary']
            except:
                try:
                    topic_response= self.process_exception(cluster)
                    cluster.topic = eval(topic_response)['topic']
                    cluster.description = eval(topic_response)['description']
                    cluster.summary = eval(topic_response)['summary']
                except:
                    cluster.topic = "OpenAI's poilicy Violation"
                    cluster.description = "OpenAI's poilicy Violation"
                    cluster.summary = "OpenAI's poilicy Violation"

    def process_exception(self, cluster):
        ranked_idx = cluster.ranked_idx.copy()
        np.random.shuffle(ranked_idx)
        text = ""
        for idx in ranked_idx[:self.topk]:
            tmp_text = cluster.data.iloc[idx]['input']
            if len(self.encoding.encode(text+tmp_text)) > self.max_token:
                break
            text += (tmp_text.strip() + "\n")
        topic_prompt = topic_template.replace("{{text}}", text)
        topic_response = self.model.retry_completion(topic_prompt)
        return topic_response

    def transform_from_dict(self, cluster_dict):
        clusters = [cluster for cluster in cluster_dict.values() if cluster.topic is None]
        topic_prompts = []
        for cluster in clusters:
            text = ""
            if len(cluster.children_id) == 0: # leaves clusters
                for idx in cluster.ranked_idx[:self.topk]:
                    tmp_text = cluster.data.iloc[idx]['input']
                    if len(self.encoding.encode(text+tmp_text)) > self.max_token:
                        break
                    text += (tmp_text.strip() + "\n")
            else:
                for id in cluster.children_id:
                    for idx in cluster_dict[id].ranked_idx[:int(self.topk/len(cluster.children_id))]:
                        tmp_text = cluster_dict[id].data.iloc[idx]['input']
                        if len(self.encoding.encode(text+tmp_text)) > self.max_token:
                            break
                        text += (tmp_text.strip() + "\n")
            topic_prompts.append(topic_template.replace("{{text}}", text))

        topic_responses = self.model.batch_completion(topic_prompts)
        for cluster, topic_response in zip(clusters, topic_responses):
            try:
                cluster.topic = eval(topic_response)['topic']
                cluster.description = eval(topic_response)['description']
                cluster.summary = eval(topic_response)['summary']
            except:
                cluster.topic = "Violation OpenAI's policy"
                cluster.description = "Violation OpenAI's policy"
                cluster.summary = "Violation OpenAI's policy"