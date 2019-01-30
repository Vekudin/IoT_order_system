import json
import unittest

from requests import HTTPError
import boto3
from moto import mock_lambda

from lambda_handlers.order_handler import lambda_handler as order_handler

event = {
  "order": {
    "car_id": "c1",
    "pickup_location": {
      "city": "Sofia",
      "housing_estate": "Studentski grad",
      "address": "Dr. Ivan Stranski 59 B"
    },
    "order_id": "o1",
    "iot_topic": "cars/calls",
    "sns_topic_arn": "arn:aws:sns:us-east-1:253712699852:orders_topic"
  }
}


class Test(unittest.TestCase):

    def test_normal_payload(self):
        lambda_cli = boto3.client('lambda')

        response = lambda_cli.invoke(
            FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(event), 'utf-8')
        )
        # Assert that function error is missing
        self.assertFalse(response.get('FunctionError'))

    def test_bad_order(self):
        self.assertRaises(HTTPError, order_handler, {'order': {'a': 13}}, "context")

    def test_unexpected_payload(self):
        self.assertRaises(HTTPError, order_handler, {'unexpected': 'payload'}, "context")


if __name__ == '__main__':
    unittest.main()
