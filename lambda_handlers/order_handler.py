import logging

from services_operations.sns_service import SnsService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Object event may have 2 fields:
    -> 'orders': list containing 'order' payload dicts which has to be transported
        to a car in order to achieve the customer's order
    -> 'car_status_configs': list containing car configurations which has to be
        set to the corresponding car's status in the ES instance"""

    sns = SnsService()

    lambda_response = {
        'status_code': 200
    }

    # (ToDo) Check if there is a free car to take the order or add the order to a queue

    # For now assume that in any order object there is an id for a free car
    sns_response = sns.publish_orders(event.get('orders'))
    lambda_response.update(sns_response)

    car_status_configs = event.get('car_status_configs')
    logger.info(f'car_status_configs:{car_status_configs}')
    # es_response = es.configure_car_status(event.get('car_status_configs'))
    # lambda_response.update(es_response)

    if len(lambda_response) is 1:
        lambda_response['status_code'] = 400
        lambda_response['body'] = "Object \"event\" contains none of the expected items"

    return lambda_response

