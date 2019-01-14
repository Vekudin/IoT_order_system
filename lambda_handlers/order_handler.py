import logging

from services_operations.sns_service import SnsService
from services_operations.es_service import EsService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

host = "es-host-here"
path = "cars/calls"


def lambda_handler(event, context):
    """Object event may have 2 fields:
    -> 'orders': list containing 'order' payload dicts which has to be transported
        to a car in order to achieve the customer's order
    -> 'car_status_configs': list containing car configurations which has to be
        set to the corresponding car's status in the ES instance"""

    sns = SnsService()
    es = EsService(host)

    orders = event.get('orders')
    car_status_data = event.get('car_status_data')

    lambda_response = {
        'status_code': 200
    }

    # The received orders represent data which tells a car to fulfill its order
    sns_response = sns.publish_orders(orders)
    lambda_response.update(sns_response)

    # Cars have received their orders and now their status must be configured
    es_response = es.update_car_status(car_status_data)
    lambda_response.update(es_response)

    if len(lambda_response) is 1:
        lambda_response['status_code'] = 400
        lambda_response['body'] = "Object \"event\" contains none of the expected items"

    return lambda_response

