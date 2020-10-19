# The base point is the order_handler.py
which is dedicated to an aws lambda function. Invoking it requires a list named 'orders' containing dicts with 'car_id'
and data of the customer's waiting location. When the corresponding car has taken the order its status is saved.
Based on aws services which is handling orders for abstract autonomous cars.

# How it works
The lambda function "order_handler" in lambda_handlers/order_handler.py is invoked with an order payload which contains
"car_id", "order_id" and "pickup_location" (example /run_scenario.py). The function sends the order to another lambda - 
"car_caller" which then sends it to the car through an iot_topic. After that "order_handler" is invoked from iot_topic
rule to confirm that the order was observed.
