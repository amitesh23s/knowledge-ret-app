import json
import os
import sys
import warnings
import environ  # new

import boto3
import botocore
from dotenv import load_dotenv
from .constants import parameters
load_dotenv()
warnings.filterwarnings('ignore')

bedrock_client = boto3.client('bedrock-runtime',region_name=os.environ.get('AWS_DEFAULT_REGION'))


class InvokeModel:
    def __init__(self, modelId):
        self.modelId = modelId

    def ask_prompt(self, prompt_data, parameters):
        body = json.dumps({"inputText": prompt_data, "textGenerationConfig": parameters})
        accept = "application/json"
        contentType = "application/json"
        try:
            
            response = bedrock_client.invoke_model(
                body=body, modelId=self.modelId, accept=accept, contentType=contentType
            )
            response_body = json.loads(response.get("body").read())
            answer = response_body.get("results")[0].get("outputText")
            return answer.strip()

        except botocore.exceptions.ClientError as error:
            if  error.response['Error']['Code'] == 'AccessDeniedException':
                print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")      
                class StopExecution(ValueError):
                    def _render_traceback_(self):
                        pass
                raise StopExecution        
            else:
                raise error


class Embeddings:
    def __init__(self, modelId):
        self.modelId = modelId

    def generate_embeddings(self, chunk):
        body = json.dumps({"inputText": chunk,})
        accept = 'application/json'
        content_type = 'application/json'

        response = bedrock_client.invoke_model(
                body=body,
                modelId=self.modelId,
                accept=accept,
                contentType=content_type )

        response_body = json.loads(response['body'].read())
        embedding = response_body.get('embedding')
        return embedding


    def store_embeddings(self, chunk):
        embedding = self.generate_embeddings(chunk)
        request_body = {
            "embeddings": embedding,
            "chunks": chunk
        }
        response  = requests.post(elastic_search_url, data = request_body)


class Context:
    def fetch_context(embedding):
        request_body = {
            "knn": {
                "field": "embeddings",
                "query_vector": embedding,
                "k": 3,
                "num_candidates": 100
            },
            "_source": ["chunks"]
        }
        response  = requests.post(elastic_search_url_fetch, json = request_body, headers = {"content-type": "application/json"})
        json_object = response.json()
        context = json_object["hits"]["hits"][0]["_source"]["chunks"]
        return context


class BuildChunks:
    def build_chunks(file):
        content = file.read()

        chunks = []
        chunk_size = 500
        i = 0
        while i<len(content):
            chunks.append(string[i: i + chunk_size])
            i += chunk_size

        return chunks