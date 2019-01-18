import unittest
import json
from requests import HTTPError

import boto3
from moto import mock_lambda

from lambda_handlers.order_handler import lambda_handler as order_handler

func_payloads = [
    {
        "order": {
            "car_id": "c1",
            "order_id": "o1",
            "pickup_location": {
                "city": "Sofia",
                "housing_estate": "Ivan Vazov",
                "address": "Some name str. 13 A"
            }
        }
    },
    {
        "order": {
            "car_id": "c2",
            "order_id": "o2",
            "pickup_location": {
                "city": "Sofia",
                "housing_estate": "Studentski grad",
                "address": "Dr. Ivan Stranski 59 A"
            }
        }
    }
]

expected_response = {
    "status_code": 200,
    "message": "The function was invoked to manage new order."
}


class Test(unittest.TestCase):
    @mock_lambda
    def test_normal_payload(self):
        lambda_cli = boto3.client('lambda')

        response = lambda_cli.invoke(
            FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(func_payloads[0]), 'utf-8')
        )
        self.assertFalse(response.get('FunctionError'))

    def test_unexpected_payload(self):
        self.assertRaises(HTTPError, order_handler, {'unexpected': 'payload'}, "context")

    def test_bad_order(self):
        self.assertRaises(HTTPError, order_handler, {'order': {'a': 13}}, "context")


if __name__ == '__main__':
    unittest.main()
