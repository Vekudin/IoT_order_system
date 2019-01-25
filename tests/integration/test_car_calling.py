import time
import os
import json
import logging

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


class Test(object):

    @classmethod
    def setup_class(cls):
        cls.iot = boto3.client('iot')
        cls.iot.create_topic_rule(
            ruleName='test_iot_topic',
            topicRulePayload={
                'sql': "SELECT * FROM 'cars/test_calls'",
                'actions': [
                    {
                        'lambda': {
                            'functionArn': 'arn:aws:lambda:us-east-1:253712699852:function:car_caller'
                        }
                    }
                ]
            }
        )

    @classmethod
    def teardown_class(cls):
        cls.iot.delete_topic_rule(
            ruleName='test_iot_topic'
        )

    @pytest.fixture()
    def lambda_cli(self):
        return boto3.client('lambda')


