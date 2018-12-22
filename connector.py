import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # At the moment the event is only supposed to be an SNS message receive
    responses = redirect_sns_messages(event.get('Records'))

    return {
        'status_code': 200,
        'body': json.dumps(responses)
    }


def redirect_sns_messages(records):
    """Redirects the received messages to a iot topic, creating a simple payload
        containing only the message."""

    print('NUMBER OF RECORDS:', len(records))
    print('records:', records)

    iot_data = boto3.client('iot-data')

    responses = []

    while records:
        message = records.pop()['Sns']['Message']
        logging.info('message: {0}'.format(message))

        payload = {
            "message": message
        }

        response = iot_data.publish(
            topic='aliens/messages',
            qos=1,
            payload=bytes(json.dumps(payload), 'utf-8')
        )
        responses.append(response)

    return responses

