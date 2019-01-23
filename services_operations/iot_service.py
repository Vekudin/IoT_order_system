import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class IotService:

    def __init__(self, topic):
        self.iot_data = boto3.client('iot-data')
        self.topic = topic

    def send_order_to_car(self, order):
        """Sends car_payload to an iot topic."""

        # Refactoring the data for the cars as it is assumed that cars would read
        # data in a different way than the service itself.
        iot_payload = {
            "car_payload": {
                'car_id': order['car_id'],
                'activity': "reach pickup location",
                'pickup_location': {
                    'city': order['pickup_location']['city'],
                    'housing_estate': order['pickup_location']['housing_estate'],
                    'address': order['pickup_location']['address']
                },
                'order_id': order['order_id']
            }
        }

        iot_response = self.iot_data.publish(
            topic=self.topic,
            qos=1,
            payload=bytes(json.dumps(iot_payload), 'utf-8')
        )

        return {
            'status_code': iot_response['ResponseMetadata']['HTTPStatusCode'],
            'order_id': order['order_id']
        }

