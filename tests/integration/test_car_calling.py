import logging
import unittest

import boto3

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
        cls.lambda_cli = boto3.client('lambda')
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
    def tearDownClass(cls):
        cls.iot.delete_topic_rule(
            ruleName='test_iot_topic'
        )



