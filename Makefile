#			Build a Lambda deployment package
#			Usage:
#			make zip


WORKING_DIR = $(shell pwd)

zip:
	@echo "Creating a deployment zip file"
	mkdir -p $(WORKING_DIR)/deploys
	zip -r $(WORKING_DIR)/deploys/lambda-site-status.zip * -x Makefile -x README.md
	cd $(VIRTUAL_ENV)/lib/python2.7/site-packages; zip -r $(WORKING_DIR)/deploys/lambda-site-status.zip requests