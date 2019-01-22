import time
import os
import json
import logging

import boto3
import pytest

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EVENT_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    'test_data',
    'sns_event.json'
)


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

    @pytest.fixture()
    def event(self):
        with open(EVENT_FILE) as file:
            event = json.loads(file.read())
            event['order']['iot_topic'] = 'cars/test_calls'
            return event

