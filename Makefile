all:
	# |Preparing order_handler.zip|
	# pip install requests --target ./config/order_handler_package
	# pip install elasticsearch --target ./config/order_handler_package
	# pip install requests_aws4auth --target ./config/order_handler_package
	cd ./config; cd ./order_handler_package; zip -r9 ../order_handler.zip .;
	zip -r ./config/order_handler.zip services_operations
	cd lambda_handlers; zip -g ../config/order_handler.zip order_handler.py
	# |Preparing car_caller.zip|
	# cd ./config; cd ./connector_package; zip -r9 ../connector.zip .;
	zip -r ./config/car_caller.zip services_operations
	cd lambda_handlers; zip -g ../config/car_caller.zip car_caller.py
	# Terraforming
	cd ./config; terraform apply;

