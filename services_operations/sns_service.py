import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SnsService:

    def __init__(self):
        self.sns = boto3.client('sns')
        self.sns_topic_arn = "arn:aws:sns:us-east-1:253712699852:orders_topic"

    def publish_order(self, order):
        """Publishes the orders data to an SNS topic."""

        # If there are no orders, then stop the flow for unneeded processes
        if not order:
            return {}

        sns_response = self.sns.publish(
            TopicArn=self.sns_topic_arn,
            Message=json.dumps(order)
        )

        return {
            'status_code': sns_response['ResponseMetadata']['HTTPStatusCode'],
            'message': "The function was invoked to manage new orders."
        }

