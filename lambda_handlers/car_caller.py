import logging

from services_operations.iot_service import IotService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

iot_topic = 'cars/calls'


def lambda_handler(event, context):
    """This function is expected to be invoked only by SNS in order to send data
    to an iot_topic. The SNS message should contains location data which has to
    be given to a car."""

    records = event.get('Records')
    if not records:
        return {
            'status_code': 400,
            'error': 'Object event contains no records or it is not a dict type.'
        }

    iot = IotService(iot_topic)

    # When lambda is invoked by SNS it always receives only one record
    response = iot.send_order_to_car(records[0])

    return response

