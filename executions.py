import json

import boto3


lambda_cli = boto3.client('lambda')

# Supported actions:
# publish -> publishes into the elasticsearch cluster
# search -> search via aws Elasticsearch

payload = {
    "sns_messages": [{'id': 'a1', 'ability': 'Smashes people\'s heads'},
                     {'id': 'a2', 'ability': 'Touches people and makes them '
                                             'explode'},
                     {'id': 'a3', 'ability': 'Transforms cows into alien '
                                             'creatures'}]
}

payload1 = {
    "search_text": "D"
}

response = lambda_cli.invoke(
    FunctionName='arn:aws:lambda:us-east-1:253712699852:function:base',
    InvocationType='Event',
    Payload=bytes(json.dumps(payload), 'utf-8')
)

print(response)
