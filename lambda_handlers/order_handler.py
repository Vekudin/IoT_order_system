import logging
from requests import HTTPError

from services_operations.sns_service import SnsService
from services_operations.es_service import EsService
from validators.new_order_validations import validate_received_order, validate_car_payload

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pending_orders = []

es_domain_endpoint = "elasticsearch-endpoint-here"


def lambda_handler(event, context):
    """Object event may have one of the following fields:
    -> 'order': list containing 'order' payload which has to be sent to an SNS
        topic in order to reach the "car_caller" lambda function
    -> 'car_payload': an iot_payload received from IoT topic Rule"""

    # New order incoming
    order = event.get('order')
    if order:
        # The received order contains car_id, order_id and pickup_location
        if not validate_received_order(order):
            raise HTTPError(400, "The structure of the received order is not "
                                 "as expected!", order)

        # Saving the order ID so that it will be checked later
        pending_orders.append(order['order_id'])
        logger.info(f"new order incoming: '{order['order_id']}'")
        logger.info(f"pending orders: {pending_orders}")

        sns = SnsService(order['sns_topic_arn'])
        response = sns.publish_order(order)

        return response

    # The function is invoked by an IoT topic rule
    car_payload = event.get('car_payload')
    if car_payload:

        if not validate_car_payload(car_payload):
            raise HTTPError(400, "The structure of the received car payload is "
                                 "not as expected!", car_payload)

        # Now data must be secured by removing the observed orders.
        logger.info(f"received car '{car_payload['car_id']}' payload with order"
                    f" id -> '{car_payload['order_id']}'")
        pending_orders.remove(car_payload['order_id'])
        logger.info(f"pending orders: {pending_orders}")

        # Saves the received car's data as a car status in ES domain
        es = EsService(es_domain_endpoint)
        es.update_car_status(car_payload)

        return {
            'status_code': 200,
            'order_id': car_payload['order_id'],
            'body': "The function was invoked to secure data."
        }

    raise HTTPError(400, "Function order_handler was invoked with unexpected "
                         "payload!", event)

