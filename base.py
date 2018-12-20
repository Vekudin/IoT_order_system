import json
import logging
import datetime

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

received_sessions = []


def lambda_handler(event, context):

    if event.get('action') == 'publish':
        # The function is invoked as a start invocation of the scenario
        responses = sns_publish(3)
        print('responses of messages: {0}'.format(responses))
    elif event.get('action') == 'clear':
        # In case if the list of sessions gets too big
        received_sessions.clear()
    else:
        # Received iot payload.
        # event = payload
        timestamp = datetime.datetime.now()
        receive_session = (timestamp, event)
        received_sessions.append(receive_session)
        print('all receive_sessions: {0}'.format(received_sessions))

    return {
        'status_code': 200,
        'body': "Okay"
    }


def sns_publish(msg_num):
    """Publishes number messages to a sns topic"""
    sns = boto3.client('sns')

    responses = []

    for i in range(msg_num):
        response = sns.publish(
            TopicArn="arn:aws:sns:us-east-1:253712699852:iot_topic",
            Message=str(i)
        )
        responses.append(response)

    return responses

