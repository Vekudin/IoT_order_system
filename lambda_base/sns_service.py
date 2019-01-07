import json

import boto3


def sns_publish(sns_messages):
    """Publishes messages to an sns topic"""
    sns = boto3.client('sns')

    # If there are no sns_messages, None would be returned
    if sns_messages is None:
        return None

    responses = []

    for m in sns_messages:
        response = sns.publish(
            TopicArn="arn:aws:sns:us-east-1:253712699852:iot_topic",
            Message=json.dumps(m)
        )
        responses.append(response)

    for r in responses:
        print("response of sns.publish():", r)
