import logging
import json

import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection


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

    def update_car_status(self, car_status):
        """Updates the car's status and target location data usually after an
        order was assigned to the vehicle."""
        # If there is no iot payload then avoid unnecessary actions
        if not car_status:
            return {}

        index = {
            "index": {
                "_index": "cars",
                "_type": "status",
                "_id": car_status.get('car_id')
            }
        }
        doc = {
            "target_location": car_status.get('target_location'),
            "activity": car_status.get('activity')
        }
        body = json.dumps(index) + "\n" + json.dumps(doc) + "\n"

        # Update the indices
        response = self.es.bulk(body=body)

        return response

    def return_free_cars(self):
        """Returns all free cars."""
        response = self.es.search(
            index='cars',
            body={
                "query": {
                    "terms": {
                        "activity": ["free"]
                    }
                }
            }
        )
        hits = response['hits']['hits']

        return hits

