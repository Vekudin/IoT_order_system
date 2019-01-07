from lambda_base import base

payload1 = {
    "action": "search",
    "search_text": "drinks touches"
}

payload = {
    "sns_messages": [{'id': 'a1', 'ability': 'Destroys people\'s heads'},
                     {'id': 'a2', 'ability': 'Touches people and makes them '
                                             'explode'},
                     {'id': 'a3', 'ability': 'Transforms cows into alien '
                                             'creatures'}]
}

lambda_response = base.lambda_handler(payload, "context")

print("\nlambda_response:", lambda_response)
