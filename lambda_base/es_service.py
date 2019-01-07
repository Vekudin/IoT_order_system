import requests

import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

region = 'us-east-1'
service = 'es'
host = 'endpoint_of_the_domain_here'
credentials = boto3.Session().get_credentials().get_frozen_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region,
                   service, session_token=credentials.token)


def search_in_domain(search_text):

    print("search_in_domain executed:", search_text)

    if search_text is None or "":
        return

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    print("here")
    response = es.search(
        index='aliens',
        body={
            "query": {
                "multi_match": {
                    "query": search_text,
                    "fields": ["ability^3", "id"]
                }
            }
        }
    )
    print("search response-->", response)
    hits = response['hits']['hits']
    print("hits-->", hits)


def put_message_to_domain(iot_payload):
    path = '/aliens/_doc/'

    # If there is no iot-payload continue
    if iot_payload is None:
        return

    print("(IN put_message_to_domain) iot_payload:", iot_payload)

    payload = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    }
    # Merging directly the received data from the iot
    payload.update(iot_payload)

    url = 'https://' + host + path + payload.get('id')

    r = requests.put(url, auth=awsauth, json=payload)
    print("(IN put_message_to_domain) r.text:", r.text)

