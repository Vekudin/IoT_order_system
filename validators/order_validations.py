from cerberus import Validator

v = Validator()


def validate_received_order(order):
    """If one of the elements is missing, False will be returned."""

    schema = {
        'car_id': {'type': 'string'},
        'pickup_location': {
            'type': 'dict',
            'allow_unknown': True,
            'schema': {
                'city': {'type': 'string'},
                'housing_estate': {'type': 'string'},
                'address': {'type': 'string'}
            }
        },
        'order_id': {'type': 'string'},
        'iot_topic': {'type': 'string'},
        'sns_topic_arn': {'type': 'string'},
    }

    return v.validate(order, schema)
