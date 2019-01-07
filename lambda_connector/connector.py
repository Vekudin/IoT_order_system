import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # The event is only supposed to be an SNS message receive
    response = sns_messages_to_iot(event.get('Records'))

    return {
        'status_code': 200,
        'body': json.dumps(response)
    }


def sns_messages_to_iot(records):
    """Redirects the received messages to an iot topic, creating a payload
        containing the received messages."""

    print('NUMBER OF RECORDS:', len(records))
    print('records:', records)

    iot_data = boto3.client('iot-data')

    iot_payload = {
        "iot_messages": []
    }

    while records:
        message = records.pop()['Sns']['Message']
        logging.info('message from records: {0}'.format(message))

        iot_payload['iot_messages'].append(message)

    # If there is empty messages data, do not use the publish function
    if iot_payload['iot_messages'] is []:
        return "There were no iot_messages stored in the payload."

    response = iot_data.publish(
        topic='aliens/messages',
        qos=1,
        payload=bytes(json.dumps(iot_payload), 'utf-8')
    )

    return response

