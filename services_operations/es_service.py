import logging
import json
import requests

import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers


logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials().get_frozen_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region,
                   service, session_token=credentials.token)


class EsService:

    def __init__(self, host):
        self.es = Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
            use_ssl=True,
            http_auth=awsauth,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

    def update_car_status(self, path, car_status_data):
        """Updates the car's status and target location data."""
        # If there is no iot-payload continue
        if not car_status_data:
            return {}

        logger.info(f"(IN put_message_to_domain) iot_payload: {car_status_data}")

        actions = [
            {
                "_index": "cars",
                "_type": "calls",
                "_id": car_status_data[i].get('car_id'),
                "_source": {
                    "status": car_status_data[i].get('status')
                }

            }
            for i in range(len(car_status_data))
        ]

        helpers.bulk(self.es, actions)


    def search_in_domain(self, search_text):
        print("search_in_domain executed:", search_text)

        if search_text is None or "":
            return

        response = self.es.search(
            index='cars',
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

