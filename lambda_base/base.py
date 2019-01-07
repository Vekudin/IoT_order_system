import logging

import lambda_base.es_service as es
import lambda_base.sns_service as sns

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # The function is invoked as a start of the scenario as there is
    # the required field in the event (sns_messages)
    sns.sns_publish(event.get('sns_messages'))

    # The function is invoked because of the iot topic rule and does operations
    # based on the field which the event contains
    es.put_message_to_domain(event.get('iot_messages'))
    es.search_in_domain(event.get('search_text'))

    return {
        'status_code': 200,
        'body': "Okay"
    }



