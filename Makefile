all:
	# |Preparing order_handler.zip|
	# pip install requests --target ./config/order_handler_package
	# pip install elasticsearch --target ./config/order_handler_package
	# pip install requests_aws4auth --target ./config/order_handler_package
	# pip install cerberus --target ./config/order_handler_package
	cd ./config; cd ./order_handler_package; zip -r9 ../order_handler.zip .;
	zip ./config/order_handler.zip services_operations/es_service.py services_operations/sns_service.py
	zip ./config/order_handler.zip validators/*.py
	cd lambda_handlers; zip -g ../config/order_handler.zip order_handler.py
	# |Preparing car_caller.zip|
	# pip install cerberus --target ./config/car_caller_package
	# pip install requests --target ./config/car_caller_package
	cd ./config; cd ./car_caller_package; zip -r9 ../car_caller.zip .;
	zip -r ./config/car_caller.zip services_operations/iot_service.py
	zip ./config/car_caller.zip validators/*.py
	cd lambda_handlers; zip -g ../config/car_caller.zip car_caller.py
	# Terraforming
	cd ./config; terraform apply;

