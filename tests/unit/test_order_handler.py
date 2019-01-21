import json
import os
from requests import HTTPError
import unittest2 as unittest

import boto3
from moto import mock_lambda

from lambda_handlers.order_handler import lambda_handler as order_handler

EVENTS_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    'test_data',
    'order_event.json'
)


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(EVENTS_FILE) as f:
            cls.event = json.loads(f.read())

    @mock_lambda
    def test_normal_payload(self):
        lambda_cli = boto3.client('lambda')

        response = lambda_cli.invoke(
            FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(self.event), 'utf-8')
        )
        # Assert that function error is missing
        self.assertFalse(response.get('FunctionError'))

    def test_bad_order(self):
        self.assertRaises(HTTPError, order_handler, {'order': {'a': 13}}, "context")

    def test_unexpected_payload(self):
        self.assertRaises(HTTPError, order_handler, {'unexpected': 'payload'}, "context")


if __name__ == '__main__':
    unittest.main()
