all:
	zip base.zip base.py
	zip connector.zip connector.py
	mv base.zip config/
	mv connector.zip config/
	echo "TEO:Zip files of the two functions ready to deploy.."
	cd config; terraform apply;
