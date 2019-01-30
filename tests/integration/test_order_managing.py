import time
import os
import json
import logging
import unittest

import boto3
import pytest

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

    @classmethod
    def setUpClass(cls):
        # cls.sns = boto3.client('sns')
        # cls.sns_test_topic_arn = cls.sns.create_topic(
        #     Name="test_orders_topic"
        # )['TopicArn']
        cls.lambda_cli = boto3.client('lambda')
        cls.event = event

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.sns.delete_topic(
        #     TopicArn=cls.sns_test_topic_arn
        # )

    def test_order_handler_to_sns_normal(self):
        response = self.lambda_cli.invoke(
            FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(self.event), 'utf-8')
        )
        payload_bytes = response.get('Payload').read()
        payload = json.loads(payload_bytes.decode('utf-8'))

        assert payload['status_code'] == 200, f"Normal one-order test failed!\n" \
            f"payload:{payload}"

    @unittest.skip("reason")
    def test_order_handler_to_car_caller(self):
        event['order']['sns_topic_arn'] = 'arn:aws:sns:us-east-1:253712699852:orders_topic'

        for i in range(4):

            event['order']['car_id'] = 'c' + str(i + 1)
            event['order']['order_id'] = 'o' + str(i + 1)

            response = self.lambda_cli.invoke(
                FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
                InvocationType='Event',
                Payload=bytes(json.dumps(self.event), 'utf-8')
            )
            logger.info(response)

            time.sleep(0.1)
