import time
import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
lambda_cli = boto3.client('lambda')

func_payloads = [
    {
        "order": {
            "car_id": "c1",
            "order_id": "o1",
            "pickup_location": {
                "city": "Sofia",
                "housing_estate": "Ivan Vazov",
                "address": "Some name str. 13 A"
            }
        }
    },
    {
        "order": {
            "car_id": "c2",
            "order_id": "o2",
            "pickup_location": {
                "city": "Sofia",
                "housing_estate": "Studentski grad",
                "address": "Dr. Ivan Stranski 59 A"
            }
        }
    }
]

for func_payload in func_payloads:
    response = lambda_cli.invoke(
        FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
        InvocationType='RequestResponse',
        Payload=bytes(json.dumps(func_payload), 'utf-8')
    )
    time.sleep(0.3)
    for k, v in response.items():
        logger.info(k, ":", v)
        if k == "Payload":
            logger.info("payload:", v.read())
