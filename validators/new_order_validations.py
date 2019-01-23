from cerberus import Validator

v = Validator()


def validate_received_order(order):
    """Validates an incoming order ."""

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


def validate_car_payload(car_payload):

    schema = {
        'car_id': {'type': 'string'},
        'activity': {'type': 'string'},
        'pickup_location': {
            'type': 'dict',
            'allow_unknown': True,
            'schema': {
                'city': {'type': 'string'},
                'housing_estate': {'type': 'string'},
                'address': {'type': 'string'}
            }
        },
        'order_id': {'type': 'string'}
    }

    return v.validate(car_payload, schema)
