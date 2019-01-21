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


class TestOrderHandler(object):
    @pytest.fixture()
    def lambda_cli(self):
        return boto3.client('lambda')

    @pytest.fixture()
    def sns(self):
        return boto3.client('sns')

    @pytest.fixture()
    def sns_test_topic_arn(self, sns):
        return sns.create_topic(
            Name="test_orders_topic"
        )['TopicArn']

    @pytest.fixture()
    def order(self, sns_test_topic_arn):
        with open(EVENT_FILE) as file:
            order = json.loads(file.read())
            order['sns_topic_arn'] = sns_test_topic_arn
            return order

    @staticmethod
    def delete_created_entities(sns, sns_test_topic_arn):
        sns.delete_topic(
            TopicArn=sns_test_topic_arn
        )

    @staticmethod
    def one_order_test(lambda_cli, order):
        response = lambda_cli.invoke(
            FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(order), 'utf-8')
        )
        payload_bytes = response.get('Payload').read()
        payload = json.loads(payload_bytes.decode('utf-8'))

        assert payload['status_code'] == 200, f"Normal one-order test failed!\n" \
            f"payload:{payload}"

    def test_handler(self, lambda_cli, sns, order, sns_test_topic_arn):
        self.one_order_test(lambda_cli, order)
        # self.multiple_order_test(...)

        self.delete_created_entities(sns, sns_test_topic_arn)
