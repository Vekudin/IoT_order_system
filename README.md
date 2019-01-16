# IoT_order_system
A system based on aws services which is handling orders for autonomous cars. The base point is the order_handler.py
which is dedicated to an aws lambda function. Invoking it requires a list named 'orders' containing dicts with 'car_id'
and data of the customer's waiting location. When the corresponding car has taken the order its status is saved.
