import base

payload1 = {
    "action": "search",
    "search_text": "people"
}

payload = {
    "action": "publish",
    "messages": [{'id': 'a1', 'ability': 'Drinks people\'s heads'},
                 {'id': 'a2', 'ability': 'Touches people and makes them fry'}]
}

lambda_response = base.lambda_handler(payload, "context")

print("\nlambda_response:", lambda_response)
