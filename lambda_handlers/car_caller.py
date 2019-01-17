import json
import logging
from requests import HTTPError

from validators import validate_received_order
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
        raise HTTPError(400, "The request cannot be handled by this function!\n"
                             "There were no records found in the event object", event)

    # When lambda is invoked by SNS it always receives only one record.
    order = json.loads(records[0]['Sns']['Message'])

    if not validate_received_order(order):
        raise HTTPError(400, "The structure of the received order is not\n"
                             "as expected!", order)

    iot = IotService(iot_topic)
    response = iot.send_order_to_car(order)

    return response

