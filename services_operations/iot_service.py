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
            'car_status_configs': []
        }

        # The SNS message is actually a list of orders
        orders = json.loads(record['Sns']['Message'])

        # Proceeding
        for order in orders:
            car_status_config = {
                'car_id': order.get('car_id'),
                'target_location': {
                    'city': order.get('city'),
                    'housing_estate': order.get('housing_state'),
                    'address': order.get('address')
                }
            }
            iot_payload['car_status_configs'].append(car_status_config)

        iot_response = self.iot_data.publish(
            topic='cars/calls',
            qos=1,
            payload=bytes(json.dumps(iot_payload), 'utf-8')
        )

        return {
            'status_code': iot_response['ResponseMetadata']['HTTPStatusCode']
        }

