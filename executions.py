import json

import boto3


lambda_cli = boto3.client('lambda')

# Supported actions:
# publish -> starts the scenario with sns publish
# clear -> clears the list of sessions
payload = {
    "action": "publish"
}

response = lambda_cli.invoke(
    FunctionName='arn:aws:lambda:us-east-1:253712699852:function:base',
    InvocationType='Event',
    Payload=bytes(json.dumps(payload), 'utf-8')
)

print(response)
