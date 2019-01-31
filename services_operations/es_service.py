import logging
import json

import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection


logging.basicConfig(level=logging.INFO)

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

    def index_new_car_status(self, car_payload):
        body = {
            "activity": car_payload['activity'],
            "pickup_location": car_payload['pickup_location'],
            "order_id": car_payload['order_id']
        }

        return self.es.index(
            index="cars_activities",
            doc_type="_doc",
            id=car_payload['car_id'],
            body=json.dumps(body)
        )

    def search_lucene(self, search_pairs):
        """Takes a dictionary with <field>:<value> as key-value pairs and returns
        a list of the found items queried with the lucene query syntax."""

        search_pairs_list = [f"{k}:{v}" for k, v in search_pairs.items()]
        q = " AND ".join(search_pairs_list)

        # index is "" as the search operation will be on all indices
        response =  self.es.search(
            index="",
            doc_type="_doc",
            q=q
        )

        return response['hits']['hits']

    def update_car_status(self, car_payload):
        """Updates the car's information and target location data usually after an
        order was assigned to the vehicle."""

        body = {
            "doc": {
                "activity": car_payload['activity'],
                "pickup_location": car_payload['pickup_location'],
                "order_id": car_payload['order_id']
            }
        }

        # Update the car's information
        response = self.es.update(
            index="cars-activities",
            doc_type='_doc',
            id=car_payload['car_id'],
            body=json.dumps(body)
        )

        return response

    def return_free_cars(self):
        """Returns a list of all free cars."""
        response = self.es.search(
            index='cars-activities',
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

