import logging
from requests import HTTPError

from services_operations.sns_service import SnsService
from validators import validate_received_order

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pending_orders = []


def lambda_handler(event, context):
    """Object event may have 2 fields:
    -> 'order': list containing 'order' payload which has to be sent to an SNS
        topic in order to reach the "car_caller" lambda function
    -> 'car_payload': an iot_payload received from IoT topic Rule"""

    order = event.get('order')
    if order:
        # The received order contains car_id, order_id and pickup_location
        if not validate_received_order(order):
            raise HTTPError(400, "The structure of the received order is not "
                                 "as expected!", order)

        # Saving the order ID so that it will be checked later
        pending_orders.append(order['order_id'])

        sns = SnsService(order['sns_topic_arn'])
        response = sns.publish_order(order)

        return response

    car_payload = event.get('car_payload')
    if car_payload:
        # Now data must be secured by removing the observed orders
        pending_orders.remove(car_payload['order_id'])

        logger.info(f"pending orders: {pending_orders}")

        return {
            'status_code': 200,
            'order_id': car_payload['order_id'],
            'body': "The function was invoked to secure data."
        }

    raise HTTPError(400, "Function order_handler was invoked with unexpected "
                         "payload!", event)

