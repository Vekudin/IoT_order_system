import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class IotService:

    def __init__(self):
        self.iot_data = boto3.client('iot-data')

    def send_data_to_cars(self, record):
        """Redirects the received messages to an iot topic, creating a payload
            containing the received messages."""

        iot_payload = {
            'car_status_data': []
        }

        # The SNS message is actually a list of orders
        orders = json.loads(record['Sns']['Message'])

        # Refactoring the data for the cars as it is expected that cars would
        # read data in a different way than the service
        for order in orders:
            car_status = {
                'car_id': order.get('car_id'),
                'target_location': {
                    'city': order.get('city'),
                    'housing_estate': order.get('housing_state'),
                    'address': order.get('address')
                },
                'status': 'reaching customer',
            }
            iot_payload['car_status_data'].append(car_status)

        iot_response = self.iot_data.publish(
            topic='cars/calls',
            qos=1,
            payload=bytes(json.dumps(iot_payload), 'utf-8')
        )

        return {
            'status_code': iot_response['ResponseMetadata']['HTTPStatusCode']
        }

