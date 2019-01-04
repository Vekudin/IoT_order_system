import json

import boto3


lambda_cli = boto3.client('lambda')

# Supported actions:
# publish -> starts the scenario with sns publish
# clear -> clears the list of sessions
# search -> search via aws Elasticsearch

payload = {
    "action": "publish",
    "messages": [{'id': 'a1', 'ability': 'Drinks people\'s heads'},
                 {'id': 'a2', 'ability': 'Touches people and makes them fry'}]
}

payload1 = {
    "action": "search",
    "search_text": "people"
}

response = lambda_cli.invoke(
    FunctionName='arn:aws:lambda:us-east-1:253712699852:function:base',
    InvocationType='Event',
    Payload=bytes(json.dumps(payload), 'utf-8')
)

print(response)
