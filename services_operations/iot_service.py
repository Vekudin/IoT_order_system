import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class IotService:

    def __init__(self, topic):
        self.iot_data = boto3.client('iot-data')
        self.topic = topic

    def send_orders_to_cars(self, record):
        """Sends iot_payload to the corresponding orders received from an SNS
        topic"""

        iot_payload = {
            'car_status_data': []
        }

        # The SNS message represents a list of orders
        orders = json.loads(record['Sns']['Message'])

        if not orders:
            return {
                'status_code': 400,
                'error': 'There is somehow an SNS message but no \'orders\' in it!'
            }

        # Refactoring the data for the cars as it is expected that cars would
        # read data in a different way than the service.
        for order in orders:
            car_status = {
                'car_id': order.get('car_id'),
                'activity': 'reaching customer',
                'target_location': {
                    'city': order.get('city'),
                    'housing_estate': order.get('housing_estate'),
                    'address': order.get('address')
                }
            }
            iot_payload['car_status_data'].append(car_status)

        iot_response = self.iot_data.publish(
            topic=self.topic,
            qos=1,
            payload=bytes(json.dumps(iot_payload), 'utf-8')
        )

        return {
            'status_code': iot_response['ResponseMetadata']['HTTPStatusCode']
        }

