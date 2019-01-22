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
    'order_event.json'
)


class Test:

    @classmethod
    def setup_class(cls):
        cls.sns = boto3.client('sns')
        cls.sns_test_topic_arn = cls.sns.create_topic(
            Name="test_orders_topic"
        )['TopicArn']
        cls.lambda_cli = boto3.client('lambda')

    @classmethod
    def teardown_class(cls):
        cls.sns.delete_topic(
            TopicArn=cls.sns_test_topic_arn
        )

    @pytest.fixture()
    def event(self):
        with open(EVENT_FILE) as file:
            event = json.loads(file.read())
            event['order']['sns_topic_arn'] = self.sns_test_topic_arn
            return event

    @pytest.mark.skip(reason="Not needed right now")
    def test_order_handler_to_sns_normal(self, event):
        response = self.lambda_cli.invoke(
            FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(event), 'utf-8')
        )
        payload_bytes = response.get('Payload').read()
        payload = json.loads(payload_bytes.decode('utf-8'))

        assert payload['status_code'] == 200, f"Normal one-order test failed!\n" \
            f"payload:{payload}"

    def test_order_handler_to_car_caller(self, event):
        event['order']['sns_topic_arn'] = 'arn:aws:sns:us-east-1:253712699852:orders_topic'

        for i in range(4):

            event['order']['car_id'] = 'c' + str(i + 1)
            event['order']['order_id'] = 'o' + str(i + 1)

            response = self.lambda_cli.invoke(
                FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
                InvocationType='Event',
                Payload=bytes(json.dumps(event), 'utf-8')
            )
            logger.info(response)
            time.sleep(0.1)
