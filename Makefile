all:
	# Preparing base.zip
	# --> pip install requests --target ./config/base_package
	# --> pip install elasticsearch --target ./config/base_package
	# --> pip install requests_aws4auth --target ./config/base_package
	cp ./base.py ./config
	# Preparing code for connector.zip
	cp ./connector.py ./config
	# Zipping base_package
	cd ./config; cd ./base_package; zip -r9 ../base.zip .;
	# implanting code into base.zip
	cd ./config; zip -g base.zip base.py;
	# Zipping connector_package
	cd ./config; cd ./connector_package; zip -r9 ../connector.zip .;
	# implanting code into connector.zip
	cd ./config; zip -g connector.zip connector.py;
	cd ./config; rm ./base.py; rm ./connector.py;
	# Terraforming
	cd ./config; terraform apply;

