import logging

from services_operations.sns_service import SnsService
from services_operations.es_service import EsService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

host = "search-cars-3uxxqnojm2h2asargsvenswncq.us-east-1.es.amazonaws.com"
path = "cars/calls"


def lambda_handler(event, context):
    """Object event may have 2 fields:
    -> 'orders': list containing 'order' payload dicts which has to be delivered
        to a car in order to reach customer's destination
    -> 'car_status_configs': list containing car configurations which has to be
        set to the corresponding car's status in the ES cluster"""

    sns = SnsService()
    es = EsService(host)

    orders = event.get('orders')
    car_status_data = event.get('car_status_data')

    lambda_response = {}

    # The received orders represent data which the car needs in order to reach
    # the customer. At this point every order has its car assigned to it (has car_id).
    sns_response = sns.publish_orders(orders)
    lambda_response.update(sns_response)

    # Cars have received their orders and now their status will be saved
    es_response = es.update_car_status(car_status_data)
    lambda_response.update(es_response)

    logger.info(lambda_response)

    if not lambda_response:
        lambda_response['status_code'] = 400
        lambda_response['body'] = "Object \"event\" contains none of the expected items"

    return lambda_response

