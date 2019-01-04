import json
import logging
import datetime
import requests

import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

logger = logging.getLogger()
logger.setLevel(logging.INFO)

received_sessions = []

region = 'us-east-1'
service = 'es'
host = 'search-aliens-hjsgrkzbyurj2los4zyt5nbuwe.us-east-1.es.amazonaws.com'
credentials = boto3.Session().get_credentials().get_frozen_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region,
                   service, session_token=credentials.token)


def lambda_handler(event, context):

    if event.get('action') == 'publish':
        # The function is invoked as a start invocation of the scenario
        messages = event.get('messages')
        responses = sns_publish(messages)
        print('responses of messages: {0}'.format(responses))
    elif event.get('action') == 'clear':
        # In case if the list of sessions gets too big
        received_sessions.clear()
    elif event.get('action') == 'search':
        search_in_domain(event.get('search_text'))
    else:
        # Received iot payload.
        # event = iot_payload
        timestamp = datetime.datetime.now()
        receive_session = (timestamp, event)
        received_sessions.append(receive_session)
        print('all receive_sessions: {0}'.format(received_sessions))

        # Directing the messages to elasticsearch domain
        direct_message_to_domain(event)

    return {
        'status_code': 200,
        'body': "Okay"
    }


def direct_message_to_domain(iot_payload):
    path = '/aliens/_doc/'

    print("(IN direct_message_to_domain) iot_payload:", iot_payload)

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
    print("(IN direct_message_to_domain) r.text:", r.text)


def search_in_domain(search_text):
    try:
        es = Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
            use_ssl=True,
            http_auth=awsauth,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    except Exception as ex:
        print("Error:", ex)

    try:
        response = es.search(
            index='aliens',
            body={
                "query": {
                    "multi_match": {
                        "query": search_text
                    }
                }
            }
        )
        print("search response-->", response)
        hits = response['hits']['hits']
        print("hits-->", hits)
    except Exception as ex:
        print("Error with search: ", ex)


def sns_publish(messages):
    """Publishes messages to an sns topic"""
    sns = boto3.client('sns')

    responses = []

    for m in messages:
        response = sns.publish(
            TopicArn="arn:aws:sns:us-east-1:253712699852:iot_topic",
            Message=json.dumps(m)
        )
        responses.append(response)

    return responses

