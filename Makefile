build_date=$(shell date --iso=seconds)
branch=$(shell git rev-parse --abbrev-ref HEAD)
commit_hash=$(shell git log -1 --pretty=format:"%H")
commit_message=$(shell git log -1 --pretty=format:"%s")
author_name=$(shell git log -n1 --format="%an")
author_date=$(shell git log -1 --pretty=format:"%ai")

present_build_metadata:
	# Structuring the collected data into the file "present_build_metadata.json"
	@echo "{" > present_build_metadata.json
	@echo "\t\"version\": \""$(version)"\"," >> present_build_metadata.json
	@echo "\t\"build_date\": \""$(build_date)"\"," >> present_build_metadata.json
	@echo "\t\"git_state\": {" >> present_build_metadata.json
	@echo "\t\t\"branch\": \""$(branch)"\"," >> present_build_metadata.json
	@echo "\t\t\"commit_hash\": \""$(commit_hash)"\"," >> present_build_metadata.json
	@echo "\t\t\"author_name\": \""$(author_name)"\"," >> present_build_metadata.json
	@echo "\t\t\"author_date\": \""$(author_date)"\"," >> present_build_metadata.json
	@echo "\t\t\"commit_message\": \""$(commit_message)"\"" >> present_build_metadata.json
	@echo "\t}" >> present_build_metadata.json
	@echo "}" >> present_build_metadata.json

	python setup.py sdist

deploy:
	# |Preparing order_handler.zip|
	# pip install requests --target ./config/order_handler_package
	# pip install elasticsearch --target ./config/order_handler_package
	# pip install requests_aws4auth --target ./config/order_handler_package
	# pip install cerberus --target ./config/order_handler_package
	cd ./config; cd ./order_handler_package; zip -r9 ../order_handler.zip .;
	zip ./config/order_handler.zip services_operations/es_service.py \
	services_operations/sns_service.py
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
