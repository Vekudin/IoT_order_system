import json
import logging

from services_operations.iot_service import IotService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """This function is expected to be invoked only by SNS. The SNS message
    should contains location data which has to be transported to a car."""

    records = event.get('Records')
    if records is None:
        return {
            'status_code': 400,
            'body': 'Object event contains no records or it is not a dict type.'
        }

    iot = IotService()

    # When lambda is invoked by SNS it always receives only one message
    lambda_response = iot.send_data_to_cars(records[0])

    return lambda_response

