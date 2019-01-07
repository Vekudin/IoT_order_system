all:
	# |Preparing base.zip|
	# -> pip install requests --target ./config/base_package
	# -> pip install elasticsearch --target ./config/base_package
	# -> pip install requests_aws4auth --target ./config/base_package
	cp ./lambda_base/*.py ./config
	# cd ./config; cd ./base_package; zip -r9 ../base.zip .;
	cd ./config; zip -g base.zip *.py;
	rm ./config/*.py
	# |Preparing connector.zip|
	cp ./lambda_connector/*.py ./config
	# cd ./config; cd ./connector_package; zip -r9 ../connector.zip .;
	cd ./config; zip -g connector.zip *.py;
	rm ./config/*.py
	# Terraforming
	cd ./config; terraform apply;

