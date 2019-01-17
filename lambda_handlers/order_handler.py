import logging
from requests import HTTPError

from services_operations.sns_service import SnsService
from services_operations.es_service import EsService
from validators import validate_received_order

logger = logging.getLogger()
logger.setLevel(logging.INFO)

host = "elasticsearch-endpoint-here"
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
            raise HTTPError("The structure of the received order is not as "
                            "expected!")

        # Saving the order ID so that they will be checked later
        pending_orders.append(order['order_id'])

        sns = SnsService()
        response = sns.publish_order(order)

        return response

    car_payload = event.get('car_payload')
    if car_payload:
        # Now data must be secured by removing the observed orders
        pending_orders.remove(car_payload['order_id'])

        logger.info(f"There are {len(pending_orders)} pending orders.")
        logger.info(f"pending orders: {pending_orders}")

        return {
            'status_code': 200,
            'message': "The function was invoked to secure data."
        }

        # es = EsService(host)
        # return es.update_car_status(car_payload)

    return {
        'status_code': 400,
        'message': "The event object does not contain order nor car_payload or"
                   " it is not a dict object."
    }

