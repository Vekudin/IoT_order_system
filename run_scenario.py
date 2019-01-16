import json

import boto3

lambda_cli = boto3.client('lambda')

payload = {
    "orders": [
        {"car_id": "c1", "city": "Sofia", "housing_estate": "Studentski grad",
         "address": "Dr. Ivan Stranski str. 59 \"A\""},
        {"car_id": "c2", "city": "Sofia", "housing_estate": "Hipodruma",
         "address": "Tsar Boris III, 81"}
    ]
}

response = lambda_cli.invoke(
    FunctionName='arn:aws:lambda:us-east-1:253712699852:function:order_handler',
    InvocationType='RequestResponse',
    Payload=bytes(json.dumps(payload), 'utf-8')
)

print(response)
